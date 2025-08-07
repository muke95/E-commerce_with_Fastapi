from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum, JSON, DateTime, text
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, server_default="1", nullable=False)
    role = Column(Enum("admin", "user", name="user_roles"), nullable=False, server_default="user")
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    carts = relationship("Cart", back_populates="user")


class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    total_amount = Column(Float, nullable=False)

    user = relationship("User", back_populates="carts")
    cart_items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    price = Column(Integer, nullable=False)
    discount_percentage = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    brand = Column(String(255), nullable=False)
    thumbnail = Column(String(1000), nullable=False)
    images = Column(JSON, nullable=False)
    is_published = Column(Boolean, server_default="1", nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
