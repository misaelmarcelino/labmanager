from alembic import op
import sqlalchemy as sa
from app.core.security import hash_password
from app.models.user import RoleEnum
# Revisão e dependências
revision = '001_create_users'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'tb_users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('role', sa.String, nullable=False, default='USER')
    )

    # Cria o admin master inicial
    bind = op.get_bind()

    bind.execute(
        sa.text("""
            INSERT INTO tb_users (name, email, password, role)
            VALUES (:name, :email, :password, :role)
        """),
        {
            "name": "Administrador Master",
            "email": "admin@labmanager.com",
            "password": hash_password("admin123"),
            "role": RoleEnum.ADMIN.value
        }
    )

def downgrade() -> None:
    op.drop_table('tb_users')
