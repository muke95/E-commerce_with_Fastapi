from fastapi import APIRouter, Depends, Query, status
from db.database import get_db
from service.products import ProductService
from sqlalchemy.orm import Session
from schemas.productService import ProductsOut ,ProductOut ,ProductCreate ,ProductUpdate,ProductOutDelete
from core.security import check_admin_role
router = APIRouter(tags=["products"], prefix="/products")


#Get all products 
@router.get("/",status_code=status.HTTP_200_OK , response_model=ProductsOut)
def get_all_product(db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based username"),
    role: str = Query("user", enum=["user", "admin"])
    ):
    return ProductService.get_all_products(db , page ,limit ,search)

# Create New Product
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
     response_model=ProductOut,
     dependencies=[Depends(check_admin_role)]
    )
def create_product(
        product: ProductCreate,
        db: Session = Depends(get_db)):
    return ProductService.create_product(db, product)


# Update Exist Product
@router.put(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductOut,
    # dependencies=[Depends(check_admin_role)]
    )
def update_product(
        product_id: int,
        updated_product: ProductUpdate,
        db: Session = Depends(get_db)):
    return ProductService.update_product(db, product_id, updated_product)


# Delete Product By ID
@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductOutDelete,
    # dependencies=[Depends(check_admin_role)]
    )
def delete_product(
        product_id: int,
        db: Session = Depends(get_db)):
    return ProductService.delete_product(db, product_id)
