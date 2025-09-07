# SOAP Implementation Guide

## C# Implementation (Recommended)

### Step 1: Add Service Reference in Visual Studio
```
1. Right-click your project → Add → Service Reference
2. Enter URL: http://your-vidyo-portal.com/services/v1_1/VidyoPortalAdminService?wsdl
3. Namespace: VidyoAdminService
4. Click OK
```

This automatically generates:
- Client proxy classes
- Data contracts
- Authentication handling
- Request/response serialization

### Step 2: Use Generated Client
```csharp
private async Task<bool> CallVidyoUpdateMemberAPI(string username, string password)
{
    try
    {
        // Create client instance (auto-generated)
        var client = new VidyoAdminService.VidyoPortalAdminServiceClient();
        
        // Set authentication
        client.ClientCredentials.UserName.UserName = txtAdminUser.Text;
        client.ClientCredentials.UserName.Password = txtAdminPassword.Text;
        
        // Get existing member
        var getMemberRequest = new VidyoAdminService.GetMemberRequest
        {
            memberID = username
        };
        var memberResponse = await client.GetMemberAsync(getMemberRequest);
        
        // Update password
        var member = memberResponse.member;
        member.password = password;
        
        var updateRequest = new VidyoAdminService.UpdateMemberRequest
        {
            memberID = username,
            member = member
        };
        
        var result = await client.UpdateMemberAsync(updateRequest);
        return result.OK == "OK";
    }
    catch (Exception ex)
    {
        LogMessage($"API Error: {ex.Message}");
        return false;
    }
}
```

## Python Implementation

### Step 1: Install SOAP Library
```bash
pip install zeep requests
```

### Step 2: Create SOAP Client
```python
from zeep import Client
from zeep.wsse.username import UsernameToken
import requests

def call_vidyo_api(self, username, password):
    try:
        # Create SOAP client from WSDL
        wsdl_url = f"{self.portal_url.get()}/services/v1_1/VidyoPortalAdminService?wsdl"
        
        # Handle SSL/TLS if needed
        session = requests.Session()
        session.verify = False  # Only if using self-signed certificates
        
        client = Client(wsdl_url, transport=Transport(session=session))
        
        # Set authentication
        client.wsse = UsernameToken(
            self.admin_user.get(), 
            self.admin_password.get()
        )
        
        # Get existing member
        member_response = client.service.GetMember(memberID=username)
        
        # Update password
        member_response.password = password
        
        # Call UpdateMember
        result = client.service.UpdateMember(
            memberID=username,
            member=member_response
        )
        
        return result == "OK"
        
    except Exception as e:
        self.log_message(f"API Error: {str(e)}")
        return False
```

## Network Requirements

### Firewall Rules (Windows Machine → Portal):
- **Outbound HTTP/HTTPS** to Vidyo Portal
- **Port 80** (HTTP) or **Port 443** (HTTPS)
- **DNS Resolution** for portal hostname

### Portal Configuration:
- **Web Services API enabled** (usually enabled by default)
- **Admin account** with API permissions
- **WSDL access** (check: http://your-portal.com/services/v1_1/VidyoPortalAdminService?wsdl)

## Authentication Flow

```
1. Windows App starts
2. User enters portal URL + admin credentials
3. App creates SOAP client pointing to portal
4. For each password change:
   a. App sends SOAP request with admin credentials
   b. Portal validates admin credentials
   c. Portal processes UpdateMember request
   d. Portal returns success/failure response
   e. App displays result to user
```

## Testing Your SOAP Connection

### Quick Test URLs:
1. **WSDL Access**: `http://your-portal.com/services/v1_1/VidyoPortalAdminService?wsdl`
   - Should return XML describing the service
   
2. **Portal Accessibility**: `http://your-portal.com`
   - Should show Vidyo Portal login page

### Common Issues:
- **WSDL not accessible**: Check portal configuration
- **Authentication failures**: Verify admin credentials
- **Network timeouts**: Check firewall rules
- **SSL/TLS errors**: Configure certificate validation

## Security Considerations

### On Windows Machine:
- Store admin credentials securely (encrypted config files)
- Use HTTPS when possible
- Validate SSL certificates
- Log operations for audit

### Network Security:
- Use VPN if accessing portal remotely
- Consider certificate-based authentication
- Monitor API usage logs on portal