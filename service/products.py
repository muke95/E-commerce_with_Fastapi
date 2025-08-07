from sqlalchemy.orm import session
from fastapi import HTTPException , status
from model.models import Product , Category
from utils.responses import ResponseHandler
from schemas.productService import ProductCreate  ,ProductUpdate



class ProductService:
    @staticmethod
    def get_all_products(db:session ,page : int , limit : int , search : str = "" , role : str = "user"):
        products = db.query(Product).order_by(Product.id.asc()).filter(Product.title.contains(search)).limit(limit).offset((page - 1) * limit).all()
        return {"message": f"Page {page} with {limit} products", "data": products}
    @staticmethod
    def create_product(db: session , product :ProductCreate ):
        category_exists = db.query(Category).filter(Category.id == product.category_id).first()
        if not category_exists:
            ResponseHandler.not_found_error("Category", product.category_id)

        product_dict = product.model_dump()
        db_product = Product(**product_dict)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return ResponseHandler.create_success(db_product.title, db_product.id, db_product)
    @staticmethod
    def update_product(db: session, product_id: int, updated_product: ProductUpdate):
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            ResponseHandler.not_found_error("Product", product_id)

        for key, value in updated_product.model_dump().items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)
        return ResponseHandler.update_success(db_product.title, db_product.id, db_product)

    @staticmethod
    def delete_product(db: session, product_id: int):
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            ResponseHandler.not_found_error("Product", product_id)
        db.delete(db_product)
        db.commit()
        return ResponseHandler.delete_success(db_product.title, db_product.id, db_product)
