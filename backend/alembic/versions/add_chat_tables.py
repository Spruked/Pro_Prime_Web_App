"""add chat tables

Revision ID: add_chat_tables
Revises: initial
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_chat_tables'
down_revision = 'initial'
branch_labels = None
depends_on = None


def upgrade():
    # Chat scripts table
    op.create_table('chat_scripts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_pattern', sa.String(length=500), nullable=False),
        sa.Column('answer', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('usage_count', sa.Integer(), nullable=True),
        sa.Column('is_learned', sa.Boolean(), nullable=True),
        sa.Column('requires_approval', sa.Boolean(), nullable=True),
        sa.Column('page_context', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_scripts_id'), 'chat_scripts', ['id'], unique=False)
    op.create_index(op.f('ix_chat_scripts_question_pattern'), 'chat_scripts', ['question_pattern'], unique=False)

    # Unanswered questions table
    op.create_table('unanswered_questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('user_session', sa.String(length=100), nullable=True),
        sa.Column('page_url', sa.String(length=500), nullable=True),
        sa.Column('suggested_answer', sa.Text(), nullable=True),
        sa.Column('is_resolved', sa.Boolean(), nullable=True),
        sa.Column('admin_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_unanswered_questions_id'), 'unanswered_questions', ['id'], unique=False)

    # Page contexts table
    op.create_table('page_contexts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('page_route', sa.String(length=200), nullable=False),
        sa.Column('page_name', sa.String(length=200), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('key_topics', sa.JSON(), nullable=True),
        sa.Column('design_notes', sa.Text(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('page_route')
    )
    op.create_index(op.f('ix_page_contexts_page_route'), 'page_contexts', ['page_route'], unique=True)


def downgrade():
    op.drop_table('page_contexts')
    op.drop_table('unanswered_questions')
    op.drop_table('chat_scripts')