# AICPA SOC 2 Trust Services Criteria (Common Criteria CC6 Series)

| Control ID | Official TSC Criteria Title | Core Regulatory Objective | Common Audit Inquiries & Exceptions |
| :--- | :--- | :--- | :--- |
| **CC6.1** | Logical Access Security & Segregation of Duties | The entity restricts logical access to provide security against unauthorized access. | Unrestricted IAM roles, developers with direct database replica access, shared production credentials. |
| **CC6.2** | User Registration, Modification, and De-provisioning | The entity controls the issuance of credentials and removes access upon termination. | Delayed offboarding tickets, inactive contractors retaining VPN access > 24h. |
| **CC6.3** | Access Entitlement & Periodic Authorization Reviews | The entity periodically reviews and re-authorizes access privileges. | Unreviewed administrator roles, privilege accumulation across departmental transfers. |
| **CC6.6** | Boundary Protection & Network Segmentation | Logical boundaries are maintained to protect confidential data and internal systems. | Production subnets directly reachable from developer staging VPCs, public SSH ports. |
| **CC6.8** | Malicious Code Protection & Unauthorized Execution | Controls prevent the introduction of malicious or unauthorized code into production. | Unsigned commits merged without peer review, bypassed CI/CD dependency vulnerability scans. |
