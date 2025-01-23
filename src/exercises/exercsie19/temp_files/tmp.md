flowchart LR
    FTP[FTP Server] --> Gather[Gather Process]
    Gather --> |"Batch of files\nafter natural break"| Monitor[Monitor Process]
    Monitor --> |Check file status| DATABASE[DATABASE System]
    DATABASE --> |File status| Monitor
    Monitor --> |"Alert if needed"| Alert[Alert System]
    
    subgraph Gather Process
    G1[Continuously monitor\nfor new files]
    G2[Collect files until\nnatural break]
    G1 --> G2
    end
    
    subgraph Monitor Process
    M1[Receive batch\nof files]
    M2[Check status in DATABASE]
    M3[Analyze status]
    M1 --> M2 --> M3
    end