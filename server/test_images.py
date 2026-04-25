from PIL import Image, ImageFilter


def apply_cutout(input_path, output_path, num_colors=100):
    # 1. פתיחת התמונה
    img = Image.open(input_path)

    # 2. המרה ל-RGB (למקרה שהתמונה בפורמט אחר)
    img = img.convert("RGB")

    # 3. החלקת התמונה (אופציונלי) - עוזר ליצור "חתיכות" גדולות ונקיות יותר
    img = img.filter(ImageFilter.MedianFilter(size=5))

    # 4. הפעלת ה-Quantize
    # colors: מספר הצבעים (השכבות)
    # dither: מוגדר כ-0 כדי למנוע נקודות וליצור משטחים חלקים
    cutout = img.quantize(colors=num_colors, dither=0)

    # 5. המרה חזרה ל-RGB ושמירה
    final_img = cutout.convert("RGB")
    final_img.save(output_path)
    print(f"האפקט הוחל בהצלחה ונשמר ב: {output_path}")


# הפעלת הפונקציה
# apply_cutout("IMG_1032.jpg", "111111111111.jpg", num_colors=5)

from PIL import Image, ImageFilter


def apply_cutout_fixed(input_path, output_path, num_colors=6):
    # פתיחת התמונה
    img = Image.open(input_path).convert("RGBA")

    # שלב חשוב: טשטוש חזק יותר כדי "לאחד" צבעים לפני הצמצום
    # אם לא נטשטש, פייתון ינסה לשמור על פרטים קטנים וזה ייראה אותו דבר
    img = img.filter(ImageFilter.BoxBlur(2))

    # שימוש ב-quantize עם שיטת Median Cut (method=2)
    # זה מאלץ את התמונה להתחלק בדיוק למספר הצבעים שביקשת
    cutout = img.quantize(colors=num_colors, method=2, dither=0)

    # שמירה כ-RGB
    final_img = cutout.convert("RGB")
    final_img.save(output_path)
    print(f"בוצע! מספר צבעים שהוגדר: {num_colors}")


# נסי להריץ פעם אחת עם 3 ופעם אחת עם 20 כדי לראות את ההבדל:
apply_cutout_fixed("IMG_9689.jpg", "result_3_colors.jpg", num_colors=13)
apply_cutout_fixed("IMG_1032.jpg", "result_20_colors.jpg", num_colors=20)


import random
from PIL import Image, ImageDraw


def apply_organic_bubbles(input_path, output_path, num_bubbles=2000):
    # 1. פתיחת התמונה
    img = Image.open(input_path).convert("RGB")
    width, height = img.size

    # 2. יצירת קנבס חדש (אפשר רקע שחור או לבן, ב-PPT זה לרוב רקע כהה)
    output_img = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(output_img)

    # 3. ציור בועות במיקומים אקראיים
    for _ in range(num_bubbles):
        # בחירת מיקום אקראי
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        # בחירת רדיוס אקראי (כדי שיהיו בועות גדולות וקטנות)
        radius = random.randint(5, 55)

        # דגימת צבע מהתמונה המקורית במיקום הזה
        color = img.getpixel((x, y))

        # הוספת שקיפות מסוימת (אופציונלי, יוצר מראה עמוק יותר)
        # כדי להשתמש בשקיפות נצטרך לעבוד עם RGBA, כאן נשתמש בצבע מלא למען הפשטות

        # 4. ציור הבועה (עיגול)
        # הבועות יחפפו כי המיקומים אקראיים לחלוטין
        draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=color
        )

    # 5. שמירה
    output_img.save(output_path)
    print(f"אפקט בועות מפוזר נוצר ב: {output_path}")


# הרצה עם כמות גדולה של בועות לכיסוי מלא
apply_organic_bubbles("IMG_9689.jpg", "organic_bubbles4.jpg", num_bubbles=15000)




# הצגה (לא חובה)
# cv2.imshow("Sketch", sketch)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
