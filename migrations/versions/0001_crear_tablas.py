"""Crea salas, estudiantes, reservas e incidencias con integridad referencial."""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("salas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(80), nullable=False),
        sa.Column("capacidad", sa.Integer(), nullable=False),
        sa.Column("ubicacion", sa.String(120), nullable=False),
        sa.Column("equipamiento", sa.JSON(), nullable=False))
    op.create_table("estudiantes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(80), nullable=False),
        sa.Column("carrera", sa.String(80), nullable=False),
        sa.Column("correo", sa.String(254), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False))
    op.create_table("reservas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sala_id", sa.Integer(), sa.ForeignKey("salas.id"), nullable=False),
        sa.Column("estudiante_id", sa.Integer(), sa.ForeignKey("estudiantes.id"), nullable=False),
        sa.Column("fecha", sa.Date(), nullable=False),
        sa.Column("hora_inicio", sa.Time(), nullable=False),
        sa.Column("hora_fin", sa.Time(), nullable=False),
        sa.Column("cantidad_personas", sa.Integer(), nullable=False),
        sa.Column("estado", sa.String(9), nullable=False))
    op.create_index("ix_reservas_sala_id", "reservas", ["sala_id"])
    op.create_index("ix_reservas_estudiante_id", "reservas", ["estudiante_id"])
    op.create_table("incidencias",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sala_id", sa.Integer(), sa.ForeignKey("salas.id"), nullable=False),
        sa.Column("reporte", sa.String(500), nullable=False),
        sa.Column("fecha", sa.Date(), nullable=False),
        sa.Column("resuelto", sa.Boolean(), nullable=False))
    op.create_index("ix_incidencias_sala_id", "incidencias", ["sala_id"])


def downgrade():
    op.drop_table("incidencias")
    op.drop_table("reservas")
    op.drop_table("estudiantes")
    op.drop_table("salas")
