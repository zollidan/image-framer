# image_api/views.py

import io
import uuid
from pathlib import Path
from PIL import Image

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status, generics
from django.conf import settings
from django.http import Http404

from .models import Image as DBImage
from .services import s3_service
from .serializer import ImageSerializer

class AddWhiteBgView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        """
        Принимает файл изображения, накладывает его на белый фон
        и возвращает URL обработанного изображения.
        """
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"detail": "File not provided."}, status=status.HTTP_400_BAD_REQUEST)

        bg_coefficient = float(request.data.get('bg_coefficient', 1.3))

        try:
            # 1. Чтение файла
            contents = file_obj.read()
            user_image = Image.open(io.BytesIO(contents)).convert("RGBA")
            original_width, original_height = user_image.size

            # 2. Вычисление новых размеров
            new_width = int(original_width * bg_coefficient)
            new_height = int(original_height * bg_coefficient)

            # 3. Создание фона
            background = Image.new("RGBA", (new_width, new_height), "WHITE")
            paste_x = (new_width - original_width) // 2
            paste_y = (new_height - original_height) // 2
            background.paste(user_image, (paste_x, paste_y), user_image)
            final_image = background.convert("RGB")

            # 6. Сохранение и загрузка в S3
            unique_id = uuid.uuid4()
            saved_filename = f"{unique_id}.jpg"
            img_byte_arr = io.BytesIO()
            final_image.save(img_byte_arr, format='JPEG')
            img_byte_arr_value = img_byte_arr.getvalue()

            s3_service.upload_object(saved_filename, img_byte_arr_value)
            result_url = f"{settings.S3_PUBLIC_URL}/{saved_filename}"

            # 7. Сохранение в БД
            DBImage.objects.create(
                original_name=file_obj.name,
                image_url=result_url
            )

            return Response({"filename": file_obj.name, "url": result_url}, status=status.HTTP_201_CREATED)

        except Image.DecompressionBombError:
            return Response({"detail": "Image size is too large."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"An error occurred during processing: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddFrameView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        """
        Принимает файл, растягивает рамку под его размер и возвращает JSON.
        """
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"detail": "File not provided."}, status=status.HTTP_400_BAD_REQUEST)

        frame_name = request.data.get('frame_name', "frame.png")
        quality = int(request.data.get('quality', 100))

        # В Django лучше использовать абсолютные пути или staticfiles
        frame_path = Path(settings.BASE_DIR) / "frames" / frame_name
        if not frame_path.is_file():
            return Response({"detail": f"Frame '{frame_name}' not found."}, status=status.HTTP_404_NOT_FOUND)

        try:

            frame_image = Image.open(frame_path)
            user_image = Image.open(file_obj)

            
            # Сохраняем оригинальные свойства
            original_size = user_image.size  # Разрешение уже сохраняется, но фиксируем
            original_icc_profile = user_image.info.get('icc_profile')
            original_exif = user_image.info.get('exif')
            original_mode = user_image.mode
            original_palette = user_image.getpalette() if original_mode == 'P' else None
            original_format = user_image.format or 'JPEG'

            # 2. Конвертируем в RGBA только для композита, если необходимо
            user_rgba = user_image.convert(
                "RGBA") if user_image.mode != "RGBA" else user_image
            frame_rgba = frame_image.convert(
                "RGBA") if frame_image.mode != "RGBA" else frame_image

            # 3. Растягиваем рамку с высококачественным ресемплингом, сохраняя оригинальное разрешение
            frame_rgba = frame_rgba.resize(
                original_size,
                resample=Image.Resampling.LANCZOS  # Высококачественный алгоритм
            )

            # 4. Создаем композитное изображение в RGBA
            combined = Image.alpha_composite(user_rgba, frame_rgba)

            # 5. Восстанавливаем оригинальный режим после композита
            if original_mode == 'P':
                # Для палитры: пытаемся квантизовать обратно, сохраняя цвета
                if original_palette:
                    combined = combined.quantize(
                        colors=256, method=2, palette=Image.ADAPTIVE)
                    # Если есть оригинальная палитра, применяем её
                    combined.putpalette(original_palette)
                else:
                    combined = combined.quantize(colors=256)
            elif original_mode == 'L':
                # Для grayscale конвертируем обратно
                combined = combined.convert('L')
            elif original_mode == 'CMYK':
                # Для CMYK: конвертируем обратно после композита
                combined = combined.convert('CMYK')
            elif original_mode == 'RGB':
                combined = combined.convert('RGB')
            elif original_mode == 'RGBA':
                # Оставляем как есть
                pass
            else:
                # По умолчанию RGB для других режимов
                combined = combined.convert('RGB')

            # 6. Восстанавливаем цветовой профиль
            if original_icc_profile:
                combined.info['icc_profile'] = original_icc_profile

            unique_id = uuid.uuid4()

            # 7. Определяем формат сохранения с приоритетом на lossless
            if original_format.upper() in ['PNG', 'WEBP', 'GIF']:
                # Для lossless форматов используем lossless сохранение
                if original_format.upper() == 'PNG':
                    saved_filename = f"{unique_id}.png"
                    save_format = "PNG"
                    save_kwargs = {
                        'optimize': True,
                        'compress_level': 1  # Минимальная компрессия для максимального качества
                    }
                elif original_format.upper() == 'WEBP':
                    saved_filename = f"{unique_id}.webp"
                    save_format = "WEBP"
                    save_kwargs = {
                        'lossless': True,
                        'quality': 100,
                        'method': 6  # Максимальное качество
                    }
                else:  # GIF или другие, сохраняем как PNG
                    saved_filename = f"{unique_id}.png"
                    save_format = "PNG"
                    save_kwargs = {
                        'optimize': True,
                        'compress_level': 1
                    }
            else:
                # Для JPEG и других используем максимальное качество
                saved_filename = f"{unique_id}.jpg"
                save_format = "JPEG"
                save_kwargs = {
                    'quality': quality if quality <= 100 else 100,
                    'optimize': False,  # Отключаем оптимизацию для сохранения качества
                    'progressive': True,
                    'subsampling': 0,  # 4:4:4 для максимального качества
                    'qtables': 'web_high'
                }

            # Добавляем EXIF если был и формат поддерживает
            if original_exif and save_format in ["JPEG", "PNG", "WEBP"]:
                save_kwargs['exif'] = original_exif

            # 8. Создаем буфер и сохраняем с настройками максимального качества
            img_byte_arr = io.BytesIO()
            combined.save(img_byte_arr, save_format, **save_kwargs)
            img_byte_arr = img_byte_arr.getvalue()

            # 9. Формируем ссылку и загружаем в S3
            result_url = f"{settings.S3_PUBLIC_URL}/{saved_filename}"
            
        
            # В конце, после загрузки в S3:
            s3_service.upload_object(saved_filename, img_byte_arr)
            result_url = f"{settings.S3_PUBLIC_URL}/{saved_filename}"

            DBImage.objects.create(
                original_name=file_obj.name,
                image_url=result_url
            )
            
            response_data = {
                "filename": file_obj.name,
                "url": result_url,
                "quality": quality,
                "format": save_format 
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Image.DecompressionBombError:
            return Response({"detail": "Image size is too large."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"An error occurred during processing: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ImagesList(generics.ListAPIView):
    """
    View to list all images in the database.
    """
    
    queryset = DBImage.objects.all()
    serializer_class = ImageSerializer
    