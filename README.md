# Vidyo Password Manager

A GUI application for managing Vidyo user passwords with month-based usernames (jan, feb, mar, etc.).

## Features

- Single user password updates
- Bulk password updates for multiple users
- Month-based username selection (jan through dec)
- Operation logging
- Progress tracking for bulk operations
- Windows-optimized interface

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