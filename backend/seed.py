import json
from app.models.database import SessionLocal, engine
from app.models.system import System
from app.models.social import SocialLink
from app.models.page import Page
from app.core.security import get_password_hash

def seed_database():
    db = SessionLocal()
    
    # Clear existing data
    db.query(System).delete()
    db.query(SocialLink).delete()
    db.query(Page).delete()
    
    # Seed systems
    systems = [
        {
            "name": "True Mark Mint",
            "slug": "true-mark-mint",
            "title": "True Mark Mint",
            "description": "Advanced digital asset minting platform with blockchain verification and smart contract integration for secure token creation.",
            "key_features": json.dumps([
                "Blockchain-based minting",
                "Smart contract automation",
                "Multi-chain support",
                "Real-time verification"
            ]),
            "learn_more_url": "https://docs.spruked.com/true-mark-mint",
            "icon": "🔷",
            "order": 1
        },
        {
            "name": "Alpha CertSig Mint",
            "slug": "alpha-certsig-mint",
            "title": "Alpha CertSig Mint",
            "description": "Certificate signature and minting system for digital credentials with cryptographic verification and immutable record keeping.",
            "key_features": json.dumps([
                "Digital certificate generation",
                "Cryptographic signatures",
                "Immutable record storage",
                "Verification API"
            ]),
            "learn_more_url": "https://docs.spruked.com/alpha-certsig",
            "icon": "📜",
            "order": 2
        },
        {
            "name": "GOAT",
            "slug": "goat",
            "title": "GOAT (Global Optimization & Analytics Tool)",
            "description": "Advanced analytics and optimization platform for complex business processes and decision-making systems.",
            "key_features": json.dumps([
                "Predictive analytics",
                "Process optimization",
                "Real-time monitoring",
                "Machine learning integration"
            ]),
            "learn_more_url": "https://docs.spruked.com/goat",
            "icon": "🐐",
            "order": 3
        },
        {
            "name": "APEX Doc",
            "slug": "apex-doc",
            "title": "APEX Doc",
            "description": "Intelligent document management and processing system with automated workflows and advanced search capabilities.",
            "key_features": json.dumps([
                "Automated document processing",
                "Intelligent search",
                "Version control",
                "Collaboration tools"
            ]),
            "learn_more_url": "https://docs.spruked.com/apex-doc",
            "icon": "📄",
            "order": 4
        },
        {
            "name": "Vault Forge",
            "slug": "vault-forge",
            "title": "Vault Forge",
            "description": "Secure data vault and encryption system for sensitive information with multi-layer security protocols.",
            "key_features": json.dumps([
                "End-to-end encryption",
                "Multi-factor authentication",
                "Audit logging",
                "Key management"
            ]),
            "learn_more_url": "https://docs.spruked.com/vault-forge",
            "icon": "🔒",
            "order": 5
        },
        {
            "name": "CALI Cognitive Systems",
            "slug": "cali-cognitive",
            "title": "CALI Cognitive Systems",
            "description": "Cognitive computing platform that mimics human thought processes for advanced problem-solving and decision support.",
            "key_features": json.dumps([
                "Neural network architecture",
                "Pattern recognition",
                "Natural language processing",
                "Cognitive learning"
            ]),
            "learn_more_url": "https://docs.spruked.com/cali-cognitive",
            "icon": "🧠",
            "order": 6
        },
        {
            "name": "Kay Gee 1.0",
            "slug": "kay-gee",
            "title": "Kay Gee 1.0",
            "description": "Knowledge graph system for interconnected data representation and intelligent relationship mapping.",
            "key_features": json.dumps([
                "Graph database integration",
                "Relationship mapping",
                "Semantic search",
                "Data visualization"
            ]),
            "learn_more_url": "https://docs.spruked.com/kay-gee",
            "icon": "🕸️",
            "order": 7
        },
        {
            "name": "Cali X One",
            "slug": "cali-x-one",
            "title": "Cali X One",
            "description": "Unified cognitive platform combining multiple AI capabilities into a single, integrated system.",
            "key_features": json.dumps([
                "Multi-AI integration",
                "Unified interface",
                "Cross-platform compatibility",
                "API-first design"
            ]),
            "learn_more_url": "https://docs.spruked.com/cali-x-one",
            "icon": "⚡",
            "order": 8
        },
        {
            "name": "ECM",
            "slug": "ecm",
            "title": "Enterprise Content Management (ECM)",
            "description": "Comprehensive content management solution for enterprise-level document and digital asset organization.",
            "key_features": json.dumps([
                "Content lifecycle management",
                "Digital asset management",
                "Workflow automation",
                "Compliance tracking"
            ]),
            "learn_more_url": "https://docs.spruked.com/ecm",
            "icon": "📊",
            "order": 9
        },
        {
            "name": "UCM",
            "slug": "ucm",
            "title": "Unified Communications Manager (UCM)",
            "description": "Centralized communications platform integrating voice, video, and messaging across multiple channels.",
            "key_features": json.dumps([
                "Multi-channel integration",
                "Real-time communications",
                "Presence management",
                "Session control"
            ]),
            "learn_more_url": "https://docs.spruked.com/ucm",
            "icon": "📞",
            "order": 10
        },
        {
            "name": "Caleon 4 Core",
            "slug": "caleon-4-core",
            "title": "Caleon 4 Core",
            "description": "Quad-core cognitive processing system for distributed intelligence and parallel computing.",
            "key_features": json.dumps([
                "Parallel processing",
                "Distributed computing",
                "Load balancing",
                "Fault tolerance"
            ]),
            "learn_more_url": "https://docs.spruked.com/caleon-4",
            "icon": "⚙️",
            "order": 11
        },
        {
            "name": "Orb Assistant",
            "slug": "orb-assistant",
            "title": "Orb Assistant",
            "description": "Intelligent virtual assistant with natural language understanding and contextual awareness.",
            "key_features": json.dumps([
                "Natural language processing",
                "Contextual awareness",
                "Task automation",
                "Learning capabilities"
            ]),
            "learn_more_url": "https://docs.spruked.com/orb-assistant",
            "icon": "🔄",
            "order": 12
        },
        {
            "name": "CALI ORB",
            "slug": "cali-orb",
            "title": "CALI ORB",
            "description": "Orchestration and routing bridge for cognitive systems, enabling seamless integration and communication.",
            "key_features": json.dumps([
                "System orchestration",
                "Intelligent routing",
                "Protocol translation",
                "Service mesh"
            ]),
            "learn_more_url": "https://docs.spruked.com/cali-orb",
            "icon": "🌐",
            "order": 13
        },
        {
            "name": "Orb-UI",
            "slug": "orb-ui",
            "title": "Orb-UI",
            "description": "Unified user interface for all CALI ecosystem components with consistent design and interaction patterns.",
            "key_features": json.dumps([
                "Unified dashboard",
                "Component library",
                "Real-time updates",
                "Responsive design"
            ]),
            "learn_more_url": "https://docs.spruked.com/orb-ui",
            "icon": "🎨",
            "order": 14
        }
    ]
    
    for system_data in systems:
        system = System(**system_data)
        db.add(system)
    
    # Seed social links
    social_links = [
        {"platform": "Twitter", "url": "https://twitter.com/proprime", "icon": "twitter", "order": 1},
        {"platform": "LinkedIn", "url": "https://linkedin.com/company/proprime", "icon": "linkedin", "order": 2},
        {"platform": "GitHub", "url": "https://github.com/proprime", "icon": "github", "order": 3},
        {"platform": "Discord", "url": "https://discord.gg/proprime", "icon": "discord", "order": 4}
    ]
    
    for link_data in social_links:
        link = SocialLink(**link_data)
        db.add(link)
    
    # Seed pages
    pages = [
        {
            "name": "home",
            "title": "Pro Prime Series Systems - Home",
            "content": "Welcome to Pro Prime Series Systems LLC, where we pioneer the future of cognitive systems and blockchain technology. Our ecosystem of interconnected technologies provides enterprise-grade solutions for the modern digital landscape.",
            "meta_description": "Pro Prime Series Systems LLC - Pioneering cognitive systems and blockchain technology"
        },
        {
            "name": "about",
            "title": "About Us - Pro Prime Series Systems",
            "content": "Pro Prime Series Systems LLC is at the forefront of technological innovation, developing cutting-edge solutions in cognitive computing, blockchain, and enterprise systems. Our mission is to provide robust, scalable, and intelligent systems that empower businesses to thrive in the digital age.",
            "meta_description": "Learn about Pro Prime Series Systems LLC and our mission"
        }
    ]
    
    for page_data in pages:
        page = Page(**page_data)
        db.add(page)
    
    db.commit()
    db.close()
    
    print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed_database()