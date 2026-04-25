# 🍽️ Shared Kitchen

> A full-stack recipe sharing platform built with Angular and Python.

## 📝 About The Project
Shared Kitchen is a comprehensive platform for sharing, discovering, and managing recipes. It features a unique **smart ingredient-matching algorithm** that helps users find recipes based on the ingredients they already have at home, minimizing the need for extra shopping.

## ✨ Key Features
* **Smart Search:** Calculates matching scores to suggest recipes based on user's available ingredients using Set intersections.
* **Role-Based Access Control:** * **Admin:** Can manage users, approve content creators, and delete recipes.
  * **Uploader:** Approved users who can add new recipes to the gallery.
  * **Reader:** Can browse, search, and view recipes.
* **Automated Image Processing:** Every uploaded recipe image is automatically processed into 3 additional variations (e.g., Grayscale, Rotated, Cropped) using Python's Pillow library.
* **Interactive Gallery:** Sort and filter recipes by preparation time, rating, and categories (Dairy, Meat, Parve).

## 💻 Technologies Used
**Frontend:**
* Angular
* HTML5 / CSS3

**Backend:**
* Python
* Flask (REST API)
* SQLite & SQLAlchemy (ORM)
* Pillow (Image Processing)

## 📌 Project Structure
The project is divided into two main parts:
* `/client` - The Angular frontend application.
* `/server` - The Python/Flask backend and database.