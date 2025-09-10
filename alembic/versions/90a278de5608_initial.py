"""initial

Revision ID: 90a278de5608
Revises:
Create Date: 2025-09-06 19:31:49.803365

"""

import geoalchemy2
import sqlalchemy as sa

from typing import Sequence, Union
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "90a278de5608"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def enum_exists(enum_name: str) -> bool:
    """Проверяет существование enum типа"""
    conn = op.get_bind()
    result = conn.execute(
        sa.text("""
            SELECT COUNT(*) 
            FROM pg_type 
            WHERE typname = :enum_name
        """),
        {"enum_name": enum_name},
    ).scalar()
    return bool(result)


def index_exists(table_name: str, index_name: str) -> bool:
    """Проверяет существование индекса"""
    conn = op.get_bind()
    result = conn.execute(
        sa.text("""
            SELECT COUNT(*) 
            FROM pg_indexes 
            WHERE tablename = :table_name 
            AND indexname = :index_name
        """),
        {"table_name": table_name, "index_name": index_name},
    ).scalar()
    return bool(result)


def upgrade() -> None:
    """Upgrade schema."""

    if not enum_exists("driver_status"):
        driver_status_enum = postgresql.ENUM(
            "active", "inactive", "banned", name="driver_status", create_type=True
        )
    else:
        driver_status_enum = postgresql.ENUM(
            "active", "inactive", "banned", name="driver_status", create_type=False
        )

    if not enum_exists("order_status"):
        order_status_enum = postgresql.ENUM(
            "driver_search",
            "waiting_driver",
            "driver_waiting_customer",
            "processing",
            "completed",
            "cancelled",
            name="order_status",
            create_type=True,
        )
    else:
        order_status_enum = postgresql.ENUM(
            "driver_search",
            "waiting_driver",
            "driver_waiting_customer",
            "processing",
            "completed",
            "cancelled",
            name="order_status",
            create_type=False,
        )

    op.create_table(
        "cities",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("base_price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column(
            "price_per_kilometer", sa.DECIMAL(precision=10, scale=2), nullable=False
        ),
        sa.Column(
            "service_commission_pct", sa.DECIMAL(precision=5, scale=2), nullable=False
        ),
        sa.Column(
            "polygon",
            geoalchemy2.types.Geometry(
                geometry_type="POLYGON",
                srid=4326,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    if not index_exists("cities", "idx_cities_polygon"):
        op.create_index(
            "idx_cities_polygon",
            "cities",
            ["polygon"],
            unique=False,
            postgresql_using="gist",
        )

    op.create_table(
        "drivers",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("middle_name", sa.String(), nullable=True),
        sa.Column("phone_number", sa.String(), nullable=False),
        sa.Column("license_number", sa.String(), nullable=False),
        sa.Column(
            "completed_orders_count", sa.Integer(), server_default="0", nullable=False
        ),
        sa.Column(
            "cancelled_orders_count", sa.Integer(), server_default="0", nullable=False
        ),
        sa.Column(
            "status", driver_status_enum, server_default="active", nullable=False
        ),
        sa.Column(
            "last_location",
            geoalchemy2.types.Geometry(
                geometry_type="POINT",
                srid=4326,
                from_text="ST_GeomFromEWKT",
                name="geometry",
            ),
            nullable=True,
        ),
        sa.Column("on_order", sa.Boolean(), server_default="False", nullable=False),
        sa.Column("on_shift", sa.Boolean(), server_default="False", nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("license_number"),
        sa.UniqueConstraint("phone_number"),
    )
    if not index_exists("drivers", "idx_drivers_last_location"):
        op.create_index(
            "idx_drivers_last_location",
            "drivers",
            ["last_location"],
            unique=False,
            postgresql_using="gist",
        )

    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("phone_number", sa.String(), nullable=False),
        sa.Column("completed_orders_count", sa.Integer(), nullable=False),
        sa.Column("cancelled_orders_count", sa.Integer(), nullable=False),
        sa.Column("roles", postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column("base_city_id", sa.UUID(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["base_city_id"],
            ["cities.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("phone_number"),
    )

    op.create_table(
        "vehicles",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("driver_id", sa.UUID(), nullable=False),
        sa.Column("brand", sa.String(), nullable=False),
        sa.Column("model", sa.String(), nullable=False),
        sa.Column("color", sa.String(), nullable=False),
        sa.Column("number", sa.String(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["driver_id"],
            ["drivers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("number"),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("customer_id", sa.UUID(), nullable=False),
        sa.Column("driver_id", sa.UUID(), nullable=True),
        sa.Column("city_id", sa.UUID(), nullable=False),
        sa.Column("points", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "status", order_status_enum, server_default="driver_search", nullable=False
        ),
        sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column(
            "service_commission", sa.DECIMAL(precision=10, scale=2), nullable=False
        ),
        sa.Column("travel_distance", sa.Integer(), nullable=False),
        sa.Column("travel_time", sa.Integer(), nullable=False),
        sa.Column("feeding_distance", sa.Integer(), nullable=True),
        sa.Column("feeding_time", sa.Integer(), nullable=True),
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["city_id"],
            ["cities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["driver_id"],
            ["drivers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("orders")
    op.drop_table("vehicles")
    op.drop_table("users")
    op.drop_index(
        "idx_drivers_last_location", table_name="drivers", postgresql_using="gist"
    )
    op.drop_table("drivers")
    op.drop_index("idx_cities_polygon", table_name="cities", postgresql_using="gist")
    op.drop_table("cities")
    # ### end Alembic commands ###
