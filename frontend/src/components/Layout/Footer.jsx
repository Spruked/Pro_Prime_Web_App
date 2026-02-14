import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  FiTwitter, 
  FiLinkedin, 
  FiGithub, 
  FiMail,
  FiFacebook,
  FiInstagram,
  FiYoutube 
} from 'react-icons/fi';
import { socialApi } from '../../services/api';

const iconMap = {
  twitter: FiTwitter,
  linkedin: FiLinkedin,
  github: FiGithub,
  email: FiMail,
  facebook: FiFacebook,
  instagram: FiInstagram,
  youtube: FiYoutube,
};

const Footer = () => {
  const [socialLinks, setSocialLinks] = useState([]);
  const currentYear = new Date().getFullYear();

  useEffect(() => {
    const fetchSocialLinks = async () => {
      try {
        const response = await socialApi.getAll();
        setSocialLinks(response.data);
      } catch (error) {
        console.error('Failed to fetch social links:', error);
      }
    };
    fetchSocialLinks();
  }, []);

  return (
    <footer className="bg-secondary/50 border-t border-white/5">
      <div className="container mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="col-span-1 md:col-span-2">
            <h3 className="text-2xl font-bold gradient-text mb-4">
              Pro Prime Series Systems
            </h3>
            <p className="text-text mb-4">
              Pioneering the future of cognitive systems and blockchain technology.
              Building the next generation of digital infrastructure.
            </p>
            <div className="flex space-x-4">
              {socialLinks.map((link) => {
                const Icon = iconMap[link.platform.toLowerCase()] || FiMail;
                return (
                  <motion.a
                    key={link.id}
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    whileHover={{ y: -3 }}
                    className="text-text hover:text-accent transition-colors"
                  >
                    <Icon size={20} />
                  </motion.a>
                );
              })}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-text-light font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li><Link to="/" className="text-text hover:text-accent transition-colors">Home</Link></li>
              <li><Link to="/systems" className="text-text hover:text-accent transition-colors">All Systems</Link></li>
              <li><Link to="/admin" className="text-text hover:text-accent transition-colors">Admin</Link></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-text-light font-semibold mb-4">Contact</h4>
            <ul className="space-y-2">
              <li className="text-text">info@spruked.com</li>
              <li className="text-text">+1 (555) 123-4567</li>
              <li className="text-text">San Francisco, CA</li>
            </ul>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-white/5 mt-8 pt-8 text-center text-text">
          <p>&copy; {currentYear} Pro Prime Series Systems LLC. All rights reserved.</p>
          <p className="text-sm mt-2">Domain: spruked.com</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;