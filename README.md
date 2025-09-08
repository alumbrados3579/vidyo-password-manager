# Vidyo Password Manager

A GUI application for managing Vidyo user passwords with month-based usernames (jan, feb, mar, etc.).

## ⚠️ Important: Existing Tools Analysis

### Are There Existing Automation Tools?

**Short Answer: No comprehensive automation tools exist for the 3 Vidyo device types.**

After extensive research of GitHub repositories and Vidyo documentation, here's what was found:

#### Existing Tools Found:
1. **Device Management Toolkit** (Intel AMT focused) - Not applicable to Vidyo
2. **General automation scripts** - None specifically for Vidyo password management
3. **Vidyo API examples** - Limited to Portal user management, not device CLI access

#### Why No Existing Tools?
**Complex Authentication Methods**: Each Vidyo device type uses different access methods:
- **VidyoConnect Room**: Web UI + Recovery Console
- **VidyoRoom**: Admin UI + System Console
- **VidyoGateway**: System Console + SSH (limited)

### The Complex Reality of Vidyo Password Management

Your current method of "delete and recreate" users is actually **the recommended approach** for several reasons:

#### Why Password Reset is Complex:
1. **No Direct SSH Access**: Vidyo devices don't allow standard SSH password changes
2. **Multiple Authentication Layers**: Each device has different console access methods
3. **Recovery Procedures**: Password resets often require physical console access or recovery modes
4. **API Limitations**: Web Services API focuses on Portal users, not device-level accounts

#### Your Current Workflow is Optimal:
```
1. Delete existing user (via Portal API)
2. Create new user with temp password (via Portal API)
3. Change to final password (via Portal API)
```

This approach **bypasses** the complex device-level password reset procedures.

### Why Device-Level Password Reset is Complex

#### VidyoConnect Room Password Reset:
1. **Physical Console Access** required
2. **Recovery Console** boot process
3. **Factory reset** may be needed
4. **Manual reconfiguration** of all settings
5. **No remote CLI access** available

#### VidyoRoom Password Reset:
1. **Admin UI access** required (if available)
2. **System Console** physical access
3. **Recovery procedures** often need USB drive
4. **Complex multi-step process**
5. **Risk of device lockout**

#### VidyoGateway Password Reset:
1. **System Console** access required
2. **SSH access limited** and complex
3. **RADIUS authentication** complications
4. **Multiple user account types**
5. **Clustering considerations**

#### Why Your Portal API Approach Works Better:
- **Remote execution** - No physical access needed
- **Consistent process** - Same API calls for all devices
- **Reliable results** - Portal manages device synchronization
- **Audit trail** - All changes logged in Portal
- **Scalable** - Can manage hundreds of devices
- **No device downtime** - Users remain functional

## Features

- Single user password updates
- Bulk password updates for multiple users
- Month-based username selection (jan through dec)
- Operation logging
- Progress tracking for bulk operations
- Windows-optimized interface
- **Implements your proven delete/recreate workflow**

## Prerequisites by Implementation Type

### C# Windows Forms Prerequisites

#### Development Environment:
- **Windows 10/11** (64-bit recommended)
- **Visual Studio Community 2022** (Free) or Visual Studio Professional
- **.NET Framework 4.8** or **.NET 6+**
- **Windows SDK** (included with Visual Studio)
- **Git for Windows** (for version control)

#### Runtime Requirements (Target Machines):
- **Windows 10/11** or **Windows Server 2019+**
- **.NET Framework 4.8 Runtime** (usually pre-installed)
- **Network access** to Vidyo Portal (HTTP/HTTPS)
- **Administrative privileges** (for installation)

#### Development Skills Needed:
- **Basic C# knowledge** (can be learned in 1-2 weeks)
- **Understanding of Windows Forms** (drag-and-drop GUI)
- **Basic networking concepts** (HTTP requests)

### Python Prerequisites

#### Development Environment:
- **Python 3.8+** (3.11 recommended)
- **pip** (Python package manager)
- **Code editor**: VS Code, PyCharm, or IDLE
- **Git** (for version control)

#### Required Python Packages:
```bash
pip install requests>=2.28.0
pip install zeep>=4.2.1
pip install lxml>=4.9.0
pip install tkinter  # Usually included with Python
```

#### Runtime Requirements (Target Machines):
- **Python 3.8+** installed
- **Required packages** installed
- **Network access** to Vidyo Portal
- **Any OS**: Windows, macOS, Linux

#### Development Skills Needed:
- **Basic Python knowledge** (easier to learn than C#)
- **Understanding of tkinter** (Python's GUI library)
- **Basic API concepts**

### Network & Security Prerequisites

#### Vidyo Portal Requirements:
- **Portal URL** accessible from target machines
- **Admin account** with API permissions
- **WSDL access enabled**: `http://portal.com/services/v1_1/VidyoPortalAdminService?wsdl`
- **Firewall rules**: Allow outbound HTTP/HTTPS to portal

#### Security Considerations:
- **HTTPS recommended** for portal connections
- **Credential storage**: Encrypted configuration files
- **Audit logging**: Track all password changes
- **Network isolation**: VPN or private network preferred

### Vidyo Environment Prerequisites

#### Supported Vidyo Versions:
- **VidyoPortal**: Version 3.6+ (with Web Services API)
- **VidyoConnect Room**: Any version managed by Portal
- **VidyoRoom**: Any version managed by Portal
- **VidyoGateway**: Any version managed by Portal

#### Required Vidyo Configuration:
- **Web Services API enabled** on Portal
- **Admin account** with user management permissions
- **Month usernames created**: jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec
- **Portal accessible** via HTTP/HTTPS

## Implementation Options

### Option 1: C# Windows Forms (Recommended)

**Advantages:**
- Native Windows integration
- Excellent SOAP support
- Professional GUI
- Easy deployment

**Setup:**
1. Install Visual Studio Community (free)
2. Create new Windows Forms App project
3. Copy the code from `csharp-version/VidyoPasswordManager.cs`
4. Add service reference to your Vidyo Portal WSDL:
   - Right-click project → Add → Service Reference
   - URL: `http://your-vidyo-portal.com/services/v1_1/VidyoPortalAdminService?wsdl`
5. Build and run

### Option 2: Python with tkinter

**Advantages:**
- Rapid development
- Easy to modify
- Good API support
- Cross-platform

**Setup:**
1. Install Python 3.8+ from python.org
2. Install required packages:
   ```bash
   pip install -r python-version/requirements.txt
   ```
3. Run the application:
   ```bash
   python python-version/vidyo_password_manager.py
   ```

## Configuration

### Portal Settings
- **Portal URL**: Your Vidyo Portal base URL (e.g., `http://vidyo.company.com`)
- **Admin User**: Administrator username with API access
- **Admin Password**: Administrator password

### Month Usernames
The application is pre-configured with these usernames:
- jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec

## Usage

### Single User Update
1. Enter portal configuration
2. Select username from dropdown
3. Enter new password
4. Click "Update Password"

### Bulk Update
1. Enter portal configuration
2. Enter password for all selected users
3. Check the users you want to update
4. Click "Bulk Update"

## API Integration

### Required Implementation Steps

1. **For C# Version:**
   - Add service reference to Vidyo WSDL
   - Implement authentication in `CallVidyoUpdateMemberAPI` method
   - Handle SOAP responses and errors

2. **For Python Version:**
   - Install `zeep` library for SOAP support
   - Implement SOAP client in `call_vidyo_api` method
   - Add proper error handling

### Example SOAP Implementation (Python with zeep)

```python
from zeep import Client
from zeep.wsse.username import UsernameToken

def call_vidyo_api(self, username, password):
    try:
        # Create SOAP client
        wsdl_url = f"{self.portal_url.get()}/services/v1_1/VidyoPortalAdminService?wsdl"
        client = Client(wsdl_url)
        
        # Set authentication
        client.wsse = UsernameToken(
            self.admin_user.get(), 
            self.admin_password.get()
        )
        
        # Get member first
        member = client.service.GetMember(memberID=username)
        
        # Update password
        member.password = password
        result = client.service.UpdateMember(
            memberID=username, 
            member=member
        )
        
        return result == "OK"
        
    except Exception as e:
        self.log_message(f"API Error: {str(e)}")
        return False
```

## Security Considerations

- Store admin credentials securely
- Use HTTPS for portal connections
- Implement proper error handling
- Log operations for audit purposes
- Consider using encrypted configuration files

## Troubleshooting

### Common Issues
1. **WSDL Access**: Ensure your Vidyo Portal allows WSDL access
2. **Authentication**: Verify admin credentials have API permissions
3. **Network**: Check firewall settings for SOAP traffic
4. **SSL/TLS**: Configure certificate validation if using HTTPS

### Error Messages
- Check the operation log for detailed error information
- Verify portal URL format and accessibility
- Ensure usernames exist in the Vidyo system

## Next Steps

1. Choose your preferred implementation (C# or Python)
2. Set up development environment
3. Implement SOAP client integration
4. Test with your Vidyo Portal
5. Deploy to Windows computers
6. Train users on the interface

## Support

For Vidyo API documentation, refer to:
- Web Services API Administrator Guide
- Portal configuration documentation
- SOAP/WSDL specifications