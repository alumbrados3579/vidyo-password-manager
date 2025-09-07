# SOAP Client Integration Architecture

## Where Everything Runs

```
┌─────────────────────────────────┐    HTTP/HTTPS    ┌─────────────────────────────────┐
│        Windows Machine          │◄─────────────────►│        Vidyo Portal             │
│                                 │   SOAP Requests   │                                 │
│  ┌─────────────────────────────┐│                   │  ┌─────────────────────────────┐│
│  │     Your GUI Application    ││                   │  │    Web Services Server      ││
│  │                             ││                   │  │                             ││
│  │  ┌─────────────────────────┐││                   │  │  ┌─────────────────────────┐││
│  │  │    SOAP Client Code     │││                   │  │  │   VidyoPortalAdminService││
│  │  │                         │││                   │  │  │                         ││
│  │  │ • Authentication        │││                   │  │  │ • UpdateMember()        ││
│  │  │ • Request Formation     │││                   │  │  │ • GetMember()           ││
│  │  │ • Response Parsing      │││                   │  │  │ • AddMember()           ││
│  │  │ • Error Handling        │││                   │  │  │ • DeleteMember()        ││
│  │  └─────────────────────────┘││                   │  │  └─────────────────────────┘││
│  └─────────────────────────────┘│                   │  └─────────────────────────────┘│
└─────────────────────────────────┘                   └─────────────────────────────────┘
           CLIENT SIDE                                            SERVER SIDE
        (You implement this)                                  (Already exists)
```

## What Runs Where

### On the Windows Machine (CLIENT SIDE - You Build This):
- **Your GUI Application** (C# or Python)
- **SOAP Client Code** that:
  - Connects to the Vidyo Portal
  - Sends authentication credentials
  - Formats SOAP requests
  - Parses SOAP responses
  - Handles errors and timeouts

### On the Vidyo Portal (SERVER SIDE - Already Exists):
- **Web Services Server** that:
  - Hosts the SOAP endpoints
  - Provides WSDL files
  - Processes incoming requests
  - Manages user database
  - Returns responses

## Communication Flow

1. **Discovery Phase** (One-time setup):
   ```
   Windows Machine → GET http://portal.com/services/v1_1/VidyoPortalAdminService?wsdl
   Portal → Returns WSDL file describing available methods
   ```

2. **Authentication & Request Phase** (Each operation):
   ```
   Windows Machine → POST SOAP Request with credentials
   Portal → Validates credentials and processes request
   Portal → Returns SOAP Response with result
   Windows Machine → Parses response and updates GUI
   ```