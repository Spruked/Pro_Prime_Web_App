import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiMenu, FiX } from 'react-icons/fi';
import { systemsApi } from '../../services/api';

const Header = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [systems, setSystems] = useState([]);
  const [scrolled, setScrolled] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchSystems = async () => {
      try {
        const response = await systemsApi.getAll();
        setSystems(response.data);
      } catch (error) {
        console.error('Failed to fetch systems:', error);
      }
    };
    fetchSystems();

    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header className={`fixed w-full z-50 transition-all duration-300 ${
      scrolled ? 'glass-effect py-4' : 'bg-transparent py-6'
    }`}>
      <nav className="container mx-auto px-6">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold gradient-text">
            PRO PRIME
          </Link>

          {/* Desktop Menu */}
          <div className="hidden lg:flex items-center space-x-8">
            <Link to="/" className="nav-link">Home</Link>
            <div className="relative group">
              <button className="nav-link flex items-center">
                Systems
                <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="absolute top-full left-0 mt-2 w-64 glass-effect rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300">
                {systems.map((system) => (
                  <Link
                    key={system.id}
                    to={`/system/${system.slug}`}
                    className="block px-4 py-2 hover:bg-accent/10 hover:text-accent transition-colors"
                  >
                    {system.title}
                  </Link>
                ))}
              </div>
            </div>
            <Link to="/admin" className="nav-link">Admin</Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="lg:hidden text-2xl"
          >
            {isOpen ? <FiX /> : <FiMenu />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="lg:hidden absolute top-full left-0 w-full glass-effect mt-2"
          >
            <div className="flex flex-col p-4 space-y-3">
              <Link to="/" className="nav-link" onClick={() => setIsOpen(false)}>Home</Link>
              <div className="space-y-2">
                <p className="text-accent font-semibold mb-2">Systems</p>
                {systems.map((system) => (
                  <Link
                    key={system.id}
                    to={`/system/${system.slug}`}
                    className="block nav-link pl-4"
                    onClick={() => setIsOpen(false)}
                  >
                    {system.title}
                  </Link>
                ))}
              </div>
              <Link to="/admin" className="nav-link" onClick={() => setIsOpen(false)}>Admin</Link>
            </div>
          </motion.div>
        )}
      </nav>
    </header>
  );
};

export default Header;