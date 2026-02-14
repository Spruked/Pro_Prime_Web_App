import json
from app.models.database import SessionLocal
from app.models.chat_models import ChatScript, PageContext

def seed_chat_data():
    """Seed initial chat scripts and page contexts"""
    db = SessionLocal()

    # Clear existing data
    db.query(ChatScript).delete()
    db.query(PageContext).delete()

    # Seed initial chat scripts
    initial_scripts = [
        {
            "question_pattern": "What is GOAT?",
            "answer": "GOAT is our comprehensive content creation platform for books, audiobooks, podcasts, and more. It provides enterprise-grade tools for content management and distribution.",
            "category": "general",
            "page_context": "global"
        },
        {
            "question_pattern": "How much does it cost",
            "answer": "Our pricing starts at $19.99 for the first GB of data processing, with tiered packages available. Contact us for a custom quote based on your needs.",
            "category": "pricing",
            "page_context": "global"
        },
        {
            "question_pattern": "What is True Mark Mint",
            "answer": "True Mark Mint is our advanced digital asset minting platform with blockchain verification and smart contract integration for secure token creation.",
            "category": "general",
            "page_context": "/system/true-mark-mint"
        },
        {
            "question_pattern": "How does Alpha CertSig Mint work",
            "answer": "Alpha CertSig Mint provides certificate signature and minting system for digital credentials with cryptographic verification and immutable record keeping.",
            "category": "technical",
            "page_context": "/system/alpha-certsig-mint"
        },
        {
            "question_pattern": "What is CALI Cognitive Systems",
            "answer": "CALI Cognitive Systems is our cognitive computing platform that mimics human thought processes for advanced problem-solving and decision support.",
            "category": "technical",
            "page_context": "/system/cali-cognitive"
        },
        {
            "question_pattern": "How do I contact you",
            "answer": "You can reach us at info@spruked.com or visit our social media channels. We're here to help with any questions about our systems and services.",
            "category": "general",
            "page_context": "global"
        },
        {
            "question_pattern": "What makes your systems different",
            "answer": "Our systems are built with cutting-edge cognitive computing, blockchain integration, and enterprise-grade security. Each system is designed to work seamlessly together as part of our CALI ecosystem.",
            "category": "general",
            "page_context": "global"
        }
    ]

    for script_data in initial_scripts:
        script = ChatScript(**script_data)
        db.add(script)

    # Seed page contexts
    page_contexts = [
        {
            "page_route": "/",
            "page_name": "Home",
            "description": "Welcome to Pro Prime Series Systems LLC - Pioneering cognitive systems and blockchain technology",
            "key_topics": ["introduction", "overview", "systems", "technology"],
            "design_notes": "Main landing page with hero section and system showcase"
        },
        {
            "page_route": "/system/true-mark-mint",
            "page_name": "True Mark Mint",
            "description": "Advanced digital asset minting platform with blockchain verification",
            "key_topics": ["blockchain", "minting", "digital assets", "smart contracts"],
            "design_notes": "Detailed system page with features and technical specifications"
        },
        {
            "page_route": "/system/cali-cognitive",
            "page_name": "CALI Cognitive Systems",
            "description": "Cognitive computing platform for advanced problem-solving",
            "key_topics": ["AI", "cognitive computing", "neural networks", "machine learning"],
            "design_notes": "Technical deep-dive page with architecture diagrams"
        }
    ]

    for context_data in page_contexts:
        context = PageContext(**context_data)
        db.add(context)

    db.commit()
    db.close()

    print("✅ Chat data seeded successfully!")

if __name__ == "__main__":
    seed_chat_data()