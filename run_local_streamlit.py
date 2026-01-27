#!/usr/bin/env python3
"""
Local Streamlit Server Runner
Run this to start local Streamlit for file upload without 403 errors
"""

import streamlit as st
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Executive Dashboard - Local",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("📊 Executive Dashboard - Local Server")
    st.markdown("---")
    
    # Import and use file upload manager
    try:
        from file_upload_manager import file_upload_manager
        from decision_engine import decision_engine
        
        # Client selection
        client_name = st.text_input("👤 Enter Client Name:", value="default")
        
        # Render file upload UI
        file_upload_manager.render_file_upload_ui(client_name)
        
        # Show AI Decision Making Section
        st.markdown("---")
        st.subheader("🧠 AI Decision Making")
        
        # Check if there's data in session state
        if 'uploaded_data' in st.session_state and st.session_state['uploaded_data'] is not None:
            st.success("✅ Data found! Generating AI decisions...")
            
            try:
                # Create data structure for decision engine
                data_for_analysis = {
                    'kpis': [],
                    'business_health_score': st.session_state.get('processed_file_data', {}).get('business_health_score', {
                        'overall': 75,
                        'financial': 75,
                        'customer': 75,
                        'operational': 75
                    }),
                    'uploaded_filename': st.session_state.get('uploaded_filename', 'unknown'),
                    'file_type': st.session_state.get('processed_file_data', {}).get('file_type', 'unknown')
                }
                
                # Generate decisions
                analysis_result = decision_engine.analyze_business_health(data_for_analysis)
                
                if analysis_result and 'prioritized_decisions' in analysis_result:
                    st.subheader("🎯 AI-Generated Business Decisions")
                    
                    decisions = analysis_result['prioritized_decisions']
                    
                    for i, decision in enumerate(decisions[:5], 1):  # Show top 5 decisions
                        with st.expander(f"Decision {i}: {decision.get('title', 'Business Decision')}"):
                            st.write(f"**Priority:** {decision.get('priority', 'Medium')}")
                            st.write(f"**Category:** {decision.get('category', 'General')}")
                            st.write(f"**Impact:** {decision.get('impact', 'Not specified')}")
                            st.write(f"**Recommendation:** {decision.get('recommendation', 'No recommendation available')}")
                            
                            # Action items
                            if 'action_items' in decision:
                                st.write("**Action Items:**")
                                for item in decision['action_items']:
                                    st.write(f"- {item}")
                    
                    # Store decisions in session state
                    st.session_state['ai_decisions'] = decisions
                    
                    # Show summary
                    st.subheader("📊 Analysis Summary")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🎯 Total Decisions", len(decisions))
                    with col2:
                        high_priority = len([d for d in decisions if d.get('priority') == 'high'])
                        st.metric("🔴 High Priority", high_priority)
                    with col3:
                        confidence = analysis_result.get('confidence_score', 0.8)
                        st.metric("🤖 Confidence", f"{confidence:.1%}")
                    
                else:
                    st.warning("⚠️ No decisions could be generated from the uploaded data")
                    
            except Exception as e:
                st.error(f"❌ Error generating decisions: {str(e)}")
                st.info("💡 Please check if the data format is correct")
        else:
            st.info("📤 Please upload a file first to generate AI decisions")
        
        # Show session state info
        if st.checkbox("🔍 Show Debug Info"):
            st.subheader("🔍 Session State Debug")
            st.json(dict(st.session_state))
            
    except ImportError as e:
        st.error(f"❌ Import Error: {e}")
        st.info("💡 Please make sure all required files are in the same directory")
    
    # Footer
    st.markdown("---")
    st.markdown("🚀 **Local Streamlit Server Running**")
    st.markdown("📁 File uploads work locally without 403 errors")
    st.markdown("🤖 AI Decision Making enabled")
    st.markdown("🔗 Next.js will connect to: http://localhost:8501")

if __name__ == "__main__":
    main()
