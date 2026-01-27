#!/usr/bin/env python3
"""
Test Environment Detection
Check if environment detection is working correctly
"""

import os

def test_environment_detection():
    """Test environment detection logic"""
    
    print("🧪 Testing Environment Detection Logic")
    print("=" * 50)
    
    # Simulate local environment
    print("\n🏠 Local Environment Test:")
    local_env = {
        'RENDER_SERVICE_ID': '',
        'HOSTNAME': '',
        'ENVIRONMENT': ''
    }
    
    is_production_local = bool(
        local_env['RENDER_SERVICE_ID'] or 
        'onrender.com' in local_env['HOSTNAME'] or
        local_env['ENVIRONMENT'] == 'production'
    )
    
    print(f"   RENDER_SERVICE_ID: '{local_env['RENDER_SERVICE_ID']}'")
    print(f"   HOSTNAME: '{local_env['HOSTNAME']}'")
    print(f"   ENVIRONMENT: '{local_env['ENVIRONMENT']}'")
    print(f"   is_production: {is_production_local}")
    print(f"   Expected: False ✅" if not is_production_local else f"   Expected: False ❌")
    
    # Simulate Render.com environment
    print("\n☁️  Render.com Environment Test:")
    render_env = {
        'RENDER_SERVICE_ID': 'svc_12345',
        'HOSTNAME': 'business-health-dashboard-1.onrender.com',
        'ENVIRONMENT': 'production'
    }
    
    is_production_render = bool(
        render_env['RENDER_SERVICE_ID'] or 
        'onrender.com' in render_env['HOSTNAME'] or
        render_env['ENVIRONMENT'] == 'production'
    )
    
    print(f"   RENDER_SERVICE_ID: '{render_env['RENDER_SERVICE_ID']}'")
    print(f"   HOSTNAME: '{render_env['HOSTNAME']}'")
    print(f"   ENVIRONMENT: '{render_env['ENVIRONMENT']}'")
    print(f"   is_production: {is_production_render}")
    print(f"   Expected: True ✅" if is_production_render else f"   Expected: True ❌")
    
    # Current actual environment
    print("\n🔍 Current Actual Environment:")
    actual_render_service_id = os.environ.get('RENDER_SERVICE_ID', 'Not Set')
    actual_hostname = os.environ.get('HOSTNAME', 'Not Set')
    actual_environment = os.environ.get('ENVIRONMENT', 'Not Set')
    
    is_production_actual = bool(
        actual_render_service_id or 
        'onrender.com' in actual_hostname or
        actual_environment == 'production'
    )
    
    print(f"   RENDER_SERVICE_ID: '{actual_render_service_id}'")
    print(f"   HOSTNAME: '{actual_hostname}'")
    print(f"   ENVIRONMENT: '{actual_environment}'")
    print(f"   is_production: {is_production_actual}")
    
    if is_production_actual:
        print(f"   Environment: Production ☁️")
        print(f"   Upload Status: Disabled ⚠️")
    else:
        print(f"   Environment: Local 🏠")
        print(f"   Upload Status: Enabled ✅")
    
    print("\n" + "=" * 50)
    print("🎯 Environment Detection Test Complete")

if __name__ == "__main__":
    test_environment_detection()
