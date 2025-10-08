# Pages module for the Streamlit app

import streamlit as st
import base64
from pathlib import Path


def render_footer():
    """Render common footer with developer info, logos, and social media links"""
    
    # Load the logos image
    logos_path = Path(__file__).resolve().parent.parent.parent / 'img' / 'logos_footnote.png'
    
    if logos_path.exists():
        with open(logos_path, 'rb') as img_file:
            logos_base64 = base64.b64encode(img_file.read()).decode()
        
        st.markdown("""
        <hr style="margin-top: 3rem; margin-bottom: 1.5rem; border: none; border-top: 2px solid #e0e0e0;">
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <style>
            .footer-link {{
                display: inline-block;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: 500;
                color: white !important;
                margin: 0 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
            }}
            .footer-link:hover {{
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                transform: translateY(-2px);
            }}
            .linkedin-link {{
                background-color: #0077B5;
            }}
            .linkedin-link:hover {{
                background-color: #006399;
            }}
            .github-link {{
                background-color: #333;
            }}
            .github-link:hover {{
                background-color: #000;
            }}
        </style>
        <div style="text-align: center; padding: 1.5rem 0; background-color: #f8f9fa; border-radius: 10px; margin: 0 -1rem;">
            <p style="margin: 0 0 1.5rem 0; font-size: 1em; color: #333; line-height: 1.6;">
                <strong>Developed by Guillem La Casta</strong><br>
                <span style="color: #666;">as part of the CSIC "Momentum Programme: Develop your Digital Talent"</span>
            </p>
            
            <div style="margin: 2rem 0;">
                <img src="data:image/png;base64,{logos_base64}" 
                     style="max-width: 90%; height: auto; margin: 0 auto; display: block; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 5px;"
                     alt="Project Logos - CSIC, ICMAN, Momentum">
            </div>
            
            <div style="margin-top: 2rem;">
                <a href="https://www.linkedin.com/in/guillemlcg" target="_blank" class="footer-link linkedin-link">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white" style="vertical-align: middle; margin-right: 8px;">
                        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                    </svg>
                    LinkedIn
                </a>
                <a href="https://github.com/guillemlcg" target="_blank" class="footer-link github-link">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white" style="vertical-align: middle; margin-right: 8px;">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                    </svg>
                    GitHub
                </a>
            </div>
            
            <p style="margin: 2rem 0 0 0; font-size: 0.85em; color: #888;">
                © 2024 Mediterranean Seagrass Project
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback without logos image
        st.markdown("""
        <style>
            .footer-link {
                display: inline-block;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: 500;
                color: white !important;
                margin: 0 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
            }
            .footer-link:hover {
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                transform: translateY(-2px);
            }
            .linkedin-link {
                background-color: #0077B5;
            }
            .linkedin-link:hover {
                background-color: #006399;
            }
            .github-link {
                background-color: #333;
            }
            .github-link:hover {
                background-color: #000;
            }
        </style>
        <hr style="margin-top: 3rem; margin-bottom: 1.5rem; border: none; border-top: 2px solid #e0e0e0;">
        <div style="text-align: center; padding: 1.5rem 0; background-color: #f8f9fa; border-radius: 10px;">
            <p style="margin: 0 0 1rem 0; font-size: 0.95em; color: #555;">
                <strong>Developed by Guillem La Casta</strong>, as part of the CSIC "Momentum Programme: Develop your Digital Talent"
            </p>
            <div style="margin-top: 1.5rem;">
                <a href="https://www.linkedin.com/in/guillemlcg" target="_blank" class="footer-link linkedin-link">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white" style="vertical-align: middle; margin-right: 8px;">
                        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                    </svg>
                    LinkedIn
                </a>
                <a href="https://github.com/guillemlcg" target="_blank" class="footer-link github-link">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white" style="vertical-align: middle; margin-right: 8px;">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                    </svg>
                    GitHub
                </a>
            </div>
            <p style="margin: 1.5rem 0 0 0; font-size: 0.85em; color: #888;">
                © 2024 Mediterranean Seagrass Project
            </p>
        </div>
        """, unsafe_allow_html=True)

