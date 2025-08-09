from sqlalchemy.orm import Session
from model.models import Category
from fastapi import HTTPException
from schemas.categoriesService import CategoryCreate, CategoryUpdate
from utils.responses import ResponseHandler


class CategoryService:
    @staticmethod
    def get_all_categories(db: Session, page: int, limit: int, search: str = ""):
        try:
            categories = (
                db.query(Category)
                .order_by(Category.id.asc())
                .filter(Category.name.contains(search))
                .limit(limit)
                .offset((page - 1) * limit)
                .all()
            )
            return {"message": f"Page {page} with {limit} categories", "data": categories}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @staticmethod
    def get_category(db: Session, category_id: int):
        try:
            category = db.query(Category).filter(Category.id == category_id).first()
            if not category:
                ResponseHandler.not_found_error("Category", category_id)
            return ResponseHandler.get_single_success(category.name, category_id, category)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @staticmethod
    def create_category(db: Session, category: CategoryCreate):
        try:
            category_dict = category.dict()
            db_category = Category(**category_dict)
            db.add(db_category)
            db.commit()
            db.refresh(db_category)
            return ResponseHandler.create_success(db_category.name, db_category.id, db_category)
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @staticmethod
    def update_category(db: Session, category_id: int, updated_category: CategoryUpdate):
        try:
            db_category = db.query(Category).filter(Category.id == category_id).first()
            if not db_category:
                ResponseHandler.not_found_error("Category", category_id)

            for key, value in updated_category.model_dump().items():
                setattr(db_category, key, value)

            db.commit()
            db.refresh(db_category)
            return ResponseHandler.update_success(db_category.name, db_category.id, db_category)
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @staticmethod
    def delete_category(db: Session, category_id: int):
        try:
            db_category = db.query(Category).filter(Category.id == category_id).first()
            if not db_category:
                ResponseHandler.not_found_error("Category", category_id)

            db.delete(db_category)
            db.commit()
            return ResponseHandler.delete_success(db_category.name, db_category.id, db_category)
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Internal Server Error")