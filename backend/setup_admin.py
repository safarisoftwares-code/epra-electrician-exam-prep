"""
Setup script to create admin user and seed the database.
Run this once after installing the application.
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Admin, User, Question
from seed_data import seed_database

def setup_admin():
    """Create default admin user"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if admin already exists
        admin = Admin.query.filter_by(username='admin').first()
        
        if not admin:
            admin = Admin(
                username='admin',
                email='safarisoftwares@gmail.com',
                full_name='System Administrator',
                role='superadmin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created successfully!")
            print("   Username: admin")
            print("   Password: admin123")
            print("   Email: safarisoftwares@gmail.com")
        else:
            print("ℹ️  Admin user already exists")
        
        # Seed questions
        print("\n📚 Seeding exam questions...")
        seed_database()
        
        print("\n✅ Setup complete!")
        print("\n📋 Summary:")
        print(f"   - Admins: {Admin.query.count()}")
        print(f"   - Questions: {Question.query.count()}")
        print(f"   - Users: {User.query.count()}")

if __name__ == '__main__':
    setup_admin()