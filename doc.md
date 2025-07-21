# Nexa Research Agent - Architecture Guide

*Complete system breakdown and technical documentation*

### **Purpose**
The Nexa Research Agent is an AI-powered research automation platform that transforms simple topic queries into comprehensive, publication-quality research reports. It delivers professional-grade research in under 30 seconds using a sophisticated pipeline of AI models, web search, and intelligent caching.

### **Core Value Proposition**
- **Speed**: Generate comprehensive reports in minutes, not hours
- **Quality**: Publication-ready content with proper citations
- **Intelligence**: Multi-model AI approach for optimal results
- **Scalability**: Handle thousands of concurrent research requests
- **Monetization**: Sustainable SaaS business model with tiered pricing

### **Key Capabilities**
- Intelligent research planning and topic breakdown
- Parallel processing of multiple research streams
- Iterative search with AI-powered refinement
- Professional content synthesis and compilation
- Real-time caching and performance optimization
- Integrated subscription management and billing

---

## Architecture Overview

### **High-Level System Design**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│   FastAPI   │───▶│   Cache     │
│ Application │    │    API      │    │   Redis     │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                    │
                           ▼                    ▼
                   ┌─────────────┐    ┌─────────────┐
                   │  Research   │    │   User DB   │
                   │  Pipeline   │    │ PostgreSQL  │
                   └─────────────┘    └─────────────┘
                           │
                           ▼
              ┌─────────────┬─────────────┐
              │             │             │
              ▼             ▼             ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │ OpenRouter  │ │   Exa.ai    │ │   Stripe    │
      │    LLMs     │ │   Search    │ │  Payments   │
      └─────────────┘ └─────────────┘ └─────────────┘
```

### **Five-Stage Research Pipeline**

| Stage | Name                  | Input           | Output              | Purpose                     |
|-------|-----------------------|-----------------|---------------------|-----------------------------|
| **1** | **Topic → LLM Plan**  | User query      | Research plan JSON  | Structured topic breakdown  |
| **2** | **Paragraph Fan-out** | Research plan   | Parallel tasks      | Concurrent processing setup |
| **3** | **Research Loop**     | Task + queries  | Research chunks     | Information gathering       |
| **4** | **Synthesis**         | Research chunks | Paragraph summaries | Content generation          |
| **5** | **Report Collation**  | All summaries   | Final report        | Professional compilation    |

### **Layered Architecture**

#### **Presentation Layer**
- **FastAPI REST API**: High-performance async endpoints
- **Interactive Documentation**: Auto-generated Swagger/ReDoc
- **Authentication System**: JWT-based user authentication
- **Rate Limiting**: Per-tier usage enforcement

#### **Business Logic Layer**
- **Research Engine**: Core pipeline orchestration
- **Planning System**: AI-powered research structuring
- **Synthesis Engine**: Content generation and compilation
- **Subscription Manager**: Tier-based feature access

#### **Service Layer**
- **LLM Integration**: OpenRouter multi-model routing
- **Search Service**: Exa.ai neural search integration
- **Payment Processing**: Stripe subscription management
- **Caching System**: Multi-layer Redis architecture

#### **Data Layer**
- **Primary Database**: PostgreSQL for persistent data
- **Cache Storage**: Redis for hot data and sessions
- **Vector Database**: Qdrant for semantic search
- **File Storage**: Temporary research artifacts

---

## Core Research Pipeline

### **Stage 1: Intelligent Planning**

#### **Purpose**
Transform a simple topic query into a structured, comprehensive research plan that ensures thorough coverage of the subject.

#### **Process Flow**
1. **Topic Analysis**: AI analyzes query scope, complexity, and research requirements
2. **Structure Generation**: Determines optimal number of sections (typically 3-7)
3. **Section Planning**: Creates detailed outlines for each research section
4. **Question Formulation**: Identifies key questions each section should answer
5. **Objective Setting**: Establishes research goals and success criteria

#### **AI Model Configuration**
- **Primary Model**: DeepSeek-R1-open
- **Temperature**: 0.6 (balanced creativity and structure)
- **Max Tokens**: 2000
- **Fallback**: Qwen-72B-instruct

#### **Output Structure**
```json
{
  "topic": "Research subject",
  "paragraphs": [
    {
      "title": "Section heading",
      "outline": "Detailed research requirements",
      "research": [],
      "latest_summary": ""
    }
  ]
}
```

#### **Quality Controls**
- Logical section progression and flow
- Comprehensive topic coverage
- Balanced depth across sections
- Clear research objectives per section

---

### **Stage 2: Parallel Task Distribution**

#### **Purpose**
Enable concurrent research across multiple topics to maximize throughput and minimize total processing time.

#### **Process Flow**
1. **Task Creation**: Convert each research section into independent task
2. **Resource Allocation**: Assign dedicated cache keys and processing slots
3. **Async Distribution**: Distribute tasks to available worker processes
4. **Progress Tracking**: Monitor completion status across all parallel streams
5. **Error Handling**: Manage failures without affecting other tasks

#### **Concurrency Design**
- **Maximum Parallel Tasks**: 7 (based on typical plan size)
- **Worker Management**: AsyncIO task pools
- **Resource Isolation**: Independent cache namespaces
- **Load Balancing**: Dynamic task distribution

#### **Coordination Mechanisms**
- **Task Status Tracking**: Real-time progress monitoring
- **Error Recovery**: Automatic retry with exponential backoff
- **Result Aggregation**: Collect completed tasks for next stage
- **Timeout Management**: Prevent hanging operations

---

### **Stage 3: Iterative Research Loop**

#### **Purpose**
Gather comprehensive, high-quality information through intelligent search and AI-powered refinement cycles.

#### **Process Flow Per Section**

##### **Initial Search Phase**
1. **Query Generation**: AI converts section outline to targeted search query
2. **Search Execution**: Exa.ai neural search with tier-based result limits
3. **Content Extraction**: Process and clean search results
4. **Quality Filtering**: Remove low-quality or irrelevant content
5. **Result Caching**: Store results for 1-week duration

##### **Reflection & Analysis Phase**
1. **Coverage Assessment**: AI analyzes results for completeness
2. **Gap Identification**: Detect missing information or weak coverage
3. **Quality Evaluation**: Assess source credibility and relevance
4. **Iteration Decision**: Determine if additional searches are needed
5. **Query Refinement**: Generate improved search terms for next iteration

##### **Iteration Management**
- **Maximum Iterations**: 3 per section (prevents infinite loops)
- **Progressive Refinement**: Each iteration builds on previous results
- **Diminishing Returns**: Stop when incremental value is low
- **Quality Thresholds**: Minimum acceptable coverage standards

#### **AI Model Usage by Phase**
- **Query Generation**: DeepSeek-R1 (temperature: 0.4)
- **Result Analysis**: Qwen-14B-chat (temperature: 0.3)
- **Refinement**: Mistral-8x7B-MoE (temperature: 0.3)

#### **Quality Assurance**
- **Source Diversity**: Ensure varied perspectives and sources
- **Fact Verification**: Cross-reference information across sources
- **Relevance Scoring**: Rank results by topic alignment
- **Content Freshness**: Prioritize recent and updated information

---

### **Stage 4: Content Synthesis**

#### **Purpose**
Transform raw research data into coherent, professional content that meets academic and professional writing standards.

#### **Paragraph-Level Synthesis**

##### **Content Processing**
1. **Research Aggregation**: Combine all research chunks for section
2. **Source Analysis**: Evaluate source quality and credibility
3. **Information Synthesis**: Merge related concepts and findings
4. **Content Generation**: Create 400-800 word professional sections
5. **Citation Integration**: Natural incorporation of source references

##### **Writing Standards**
- **Academic Tone**: Professional, objective writing style
- **Logical Structure**: Clear introduction, body, and conclusions
- **Smooth Transitions**: Coherent flow between concepts
- **Evidence-Based**: Claims supported by research findings
- **Proper Attribution**: Natural citation of sources

#### **Quality Features**
- **Fact-Checking**: Verification across multiple sources
- **Consistency**: Uniform tone and style throughout
- **Clarity**: Accessible language for target audience
- **Completeness**: Addresses all outline requirements

#### **AI Configuration**
- **Primary Model**: Claude-3-Haiku
- **Temperature**: 0.2 (prioritize accuracy and consistency)
- **Max Tokens**: 1500 per section
- **Style Guidelines**: Academic/professional writing standards

---

### **Stage 5: Final Report Compilation**

#### **Purpose**
Create a cohesive, publication-ready research report that synthesizes all sections into a comprehensive document.

#### **Report Assembly Process**

##### **Structure Creation**
1. **Executive Summary**: Concise overview of key findings
2. **Introduction**: Context setting and scope definition
3. **Section Integration**: Smooth compilation of all research sections
4. **Transition Generation**: Create logical bridges between sections
5. **Conclusion**: Synthesis of findings and implications

##### **Enhancement Features**
- **Professional Formatting**: Proper markdown structure and hierarchy
- **Bibliography Generation**: Comprehensive source listing
- **Word Count Optimization**: Target 1500-3000 words
- **Quality Assurance**: Final review and polish

#### **Report Standards**
- **Publication Quality**: Ready for professional use
- **Comprehensive Coverage**: Thorough treatment of topic
- **Accessible Language**: Clear for target audience
- **Proper Citations**: Full source attribution

#### **AI Configuration**
- **Primary Model**: Claude-3-Sonnet (Pro+ users)
- **Fallback Model**: DeepSeek-R1-open (Free users)
- **Temperature**: 0.3 (balanced creativity and accuracy)
- **Max Tokens**: 4000 for comprehensive compilation

---

## AI Model Strategy

### **Multi-Model Architecture Philosophy**

The system employs a specialized multimodel approach where different AI models are optimized for specific tasks in the research pipeline. This approach maximizes quality while controlling costs and latency.

### **Model Selection Criteria**
- **Task Specialization**: Models chosen for specific cognitive strengths
- **Cost Optimization**: Balance quality with API usage costs
- **Performance**: Response time and throughput considerations
- **Reliability**: Fallback options for high availability

### **Model Routing Matrix**

| Task Type        | Primary Model    | Strengths                                | Use Case               | Fallback          |
|------------------|------------------|------------------------------------------|------------------------|-------------------|
| **Reasoning**    | DeepSeek-R1-open | Logical analysis, structured thinking    | Research planning      | Qwen-72B-instruct |
| **Search Query** | DeepSeek-R1-open | Intent understanding, query optimization | Search term generation | Same as primary   |
| **Analysis**     | Qwen-14B-chat    | Content evaluation, critical thinking    | Result assessment      | Mistral-8x7B-MoE  |
| **Synthesis**    | Claude-3-Haiku   | High-quality text generation             | Content creation       | Mixtral-8x7B      |
| **Compilation**  | Claude-3-Sonnet  | Long-form coherent writing               | Final assembly         | DeepSeek-R1-open  |

### **Temperature Settings by Task**

| Task               | Temperature | Reasoning                         |
|--------------------|-------------|-----------------------------------|
| **Planning**       | 0.5-0.7     | Balanced structure and creativity |
| **Search Queries** | 0.4         | Focused and precise               |
| **Reflection**     | 0.3         | Analytical and consistent         |
| **Synthesis**      | 0.2         | Accurate and professional         |
| **Compilation**    | 0.3         | Coherent with subtle creativity   |

### **Intelligent Fallback System**

#### **Failure Detection**
- API timeout monitoring
- Response quality validation
- Error rate tracking
- Performance degradation detection

#### **Fallback Strategy**
1. **Immediate Fallback**: Switch to back up model on failure
2. **Quality Verification**: Validate fallback response quality
3. **User Transparency**: Optional notification of model switches
4. **Performance Logging**: Track fallback usage for optimization

### **Token Management**

#### **Tier-Based Limits**
- **Free**: 4K tokens per request
- **Pro**: 32K tokens per request  
- **Custom**: 128K tokens per request

#### **Optimization Techniques**
- **Dynamic Truncation**: Intelligent content summarization
- **Chunking Strategy**: Break large requests into optimal sizes
- **Context Prioritization**: Most important information first
- **Progressive Enhancement**: Add detail based on available tokens

---

## Search Intelligence

### **Exa.ai Neural Search Integration**

#### **Core Capabilities**
- **Semantic Understanding**: Natural language query processing
- **Content Extraction**: Full webpage content retrieval
- **Relevance Scoring**: AI-powered result ranking
- **Domain Intelligence**: Source quality assessment

#### **Search Configuration**

```json
{
  "query": "generated_search_term",
  "num_results": "tier_based_limit",
  "include_domains": [],
  "exclude_domains": ["reddit.com", "twitter.com", "forum_sites"],
  "start_crawl_date": "2020-01-01",
  "end_crawl_date": "current_date",
  "use_autoprompt": true,
  "type": "neural",
  "contents": {
    "text": {"max_characters": 2000}
  }
}
```

#### **Quality Controls**
- **Source Filtering**: Exclude low-quality domains
- **Content Validation**: Verify relevance and accuracy
- **Duplicate Detection**: Remove redundant information
- **Freshness Priority**: Favor recent and updated content

### **Search Strategy Architecture**

#### **Multi-Phase Search Approach**

##### **Phase 1: Broad Discovery**
- **Objective**: Establish comprehensive topic coverage
- **Query Style**: Broad, inclusive search terms
- **Result Target**: Maximum allowed results per tier
- **Focus**: Breadth over depth

##### **Phase 2: Targeted Deep-Dive**
- **Objective**: Fill specific information gaps
- **Query Style**: Narrow, specific search terms
- **Result Target**: Focused result sets
- **Focus**: Depth and specificity

##### **Phase 3: Verification & Validation**
- **Objective**: Confirm key facts and findings
- **Query Style**: Fact-checking and cross-reference queries
- **Result Target**: Authoritative sources
- **Focus**: Accuracy and credibility

### **Intelligent Query Generation**

#### **Query Optimization Process**
1. **Context Analysis**: Understand section requirements
2. **Term Extraction**: Identify key concepts and keywords
3. **Query Construction**: Build effective search strings
4. **Refinement Logic**: Improve based on previous results
5. **Iteration Strategy**: Plan follow-up searches

#### **Query Types by Research Phase**
- **Exploratory**: "AI healthcare diagnostics overview"
- **Specific**: "machine learning medical imaging accuracy 2024"
- **Comparative**: "AI vs traditional diagnostic methods"
- **Statistical**: "healthcare AI adoption rates statistics"
- **Case Study**: "successful AI diagnostic implementations"

### **Advanced Caching Strategy**

#### **Three-Layer Cache Architecture**

##### **Layer 1: Query Result Cache**
- **Scope**: Individual search results
- **TTL**: 1 week (604,800 seconds)
- **Key Format**: `search:sha256(query)`
- **Benefits**: Reduced API costs, faster responses

##### **Layer 2: Processed Content Cache**
- **Scope**: Cleaned and processed search content
- **TTL**: 3 days (259,200 seconds)  
- **Key Format**: `content:sha256(url+timestamp)`
- **Benefits**: Skip content processing overhead

##### **Layer 3: Research Chunk Cache**
- **Scope**: Complete research chunks with analysis
- **TTL**: Session-based (until report completion)
- **Key Format**: `chunk:task_id:iteration`
- **Benefits**: Enable resume from interruption

#### **Cache Optimization Features**
- **Intelligent Prefetching**: Predict and cache likely queries
- **Usage Analytics**: Track cache hit rates and optimize
- **Memory Management**: LRU eviction with size limits
- **Cross-User Benefits**: Popular topics cached for all users

---

## Monetization Strategy

### **Three-Tier SaaS Model**

The monetization strategy is built around a freemium model with clear value progression that encourages natural user upgrades based on usage patterns and feature needs.

#### **Free Tier - User Acquisition**

**Purpose**: Attract users and demonstrate value

**Limitations**:
- 10 queries per day (sufficient for casual use)
- 4K token limit per request (shorter reports)
- 5 search results per query (basic research depth)
- 24-hour cache duration (limited reuse)
- Top 3 vector chunks (reduced context)

**Value Proposition**:
- Full pipeline access
- Professional-quality reports
- No credit card required
- Immediate value demonstration

#### **Pro Tier - Primary Revenue ($29/month)**

**Purpose**: Serve power users and small businesses

**Enhancements**:
- 200 queries per day (20x increase)
- 32K token limit (8x longer reports)
- 10 search results per query (2x research depth)
- 72-hour cache duration (3x reuse value)
- Top 10 vector chunks (enhanced context)
- Email support

**Target Users**:
- Content creators and marketers
- Small business researchers
- Academic professionals
- Consultants and analysts

#### **Custom Tier - Enterprise Revenue (Custom Pricing)**

**Purpose**: Serve enterprise customers with unlimited needs

**Features**:
- Unlimited daily queries
- 128K token limit (enterprise-length reports)
- 20 search results per query (maximum depth)
- 7-day cache duration (week-long projects)
- Full vector search capability
- Priority support with SLA
- Custom integrations available

**Target Users**:
- Large enterprises
- Research institutions
- Government agencies
- High-volume content operations

### **Stripe Integration Architecture**

#### **Customer Lifecycle Management**

##### **Onboarding Flow**
1. **Free Registration**: Create account without payment
2. **Usage Tracking**: Monitor query patterns and limits
3. **Upgrade Prompts**: Strategic upgrade suggestions
4. **Seamless Checkout**: One-click Stripe integration
5. **Immediate Access**: Instant tier upgrades

##### **Subscription Management**
- **Automatic Billing**: Recurring subscription handling
- **Proration**: Mid-cycle upgrade/downgrade calculations
- **Failed Payments**: Grace periods and retry logic
- **Cancellation**: Retain access until period end

#### **Technical Implementation**

##### **Webhook Event Handling**
```
checkout.session.completed → Upgrade user tier
customer.subscription.updated → Modify access levels
customer.subscription.deleted → Downgrade to free
invoice.payment_failed → Implement grace period
invoice.payment_succeeded → Confirm continued access
```

##### **Customer Portal Integration**
- **Self-Service**: Users manage subscriptions independently
- **Billing History**: Complete transaction records
- **Plan Changes**: Upgrade/downgrade options
- **Payment Methods**: Update cards and billing info

### **Usage Enforcement System**

#### **Real-Time Quota Management**

##### **Daily Limit Tracking**
- **Counter Storage**: Redis with daily expiration
- **Atomic Operations**: Prevent race conditions
- **Real-Time Checks**: Before each query execution
- **Graceful Degradation**: Clear limit notifications

##### **Feature Access Control**
```python
tier_limits = {
    "free": {"queries": 10, "tokens": 4000, "searches": 5},
    "pro": {"queries": 200, "tokens": 32000, "searches": 10},
    "custom": {"queries": 10000, "tokens": 128000, "searches": 20}
}
```

#### **Upgrade Conversion Strategy**

##### **Strategic Limit Notifications**
- **Approaching Limits**: 80% usage warnings
- **Limit Reached**: Clear upgrade benefits
- **Feature Previews**: Show what Pro/Custom enables
- **Timing**: Present upgrades at high-value moments

##### **Value Demonstration**
- **Quality Comparisons**: Show enhanced features in action
- **ROI Calculations**: Demonstrate time and cost savings
- **Success Stories**: Case studies and testimonials
- **Free Trials**: Limited-time Pro access for evaluation

---

## Data Architecture

### **Multi-Database Strategy**

The system employs a polyglot persistence approach, using different databases optimized for specific data types and access patterns.

#### **PostgreSQL - Primary Transactional Data**

**Purpose**: ACID-compliant storage for critical business data

**Schema Design**:

```sql
-- Users and authentication
users (id, email, tier, stripe_customer_id, created_at, last_login)

-- Subscription management  
subscriptions (id, user_id, stripe_subscription_id, tier, status, created_at)

-- Query history and analytics
queries (id, user_id, topic, tier, word_count, duration, created_at)

-- Administrative and audit logs
admin_actions (id, admin_id, action, target, details, timestamp)
```

**Optimization Features**:
- **Indexing Strategy**: Composite indexes on user_id + created_at
- **Partitioning**: Monthly partitions for query history
- **Connection Pooling**: PgBouncer for connection management
- **Read Replicas**: Separate analytics queries from transactional load

#### **Redis - High-Performance Caching**

**Purpose**: Sub-millisecond data access for hot data and session management

**Data Structures**:

```redis
# Report caching
"report:sha256(user_id:topic)" → JSON report data

# Search result caching  
"search:sha256(query)" → HASH of search results

# Rate limiting
"queries:user_id:YYYY-MM-DD" → daily counter with TTL

# Session state
"session:session_id" → HASH of user session data
```

**Memory Management**:
- **Eviction Policy**: LRU for optimal memory usage
- **Memory Limits**: Tier-based allocation
- **Persistence**: RDB snapshots for disaster recovery
- **Clustering**: Redis Cluster for horizontal scaling

#### **Qdrant - Vector Search Database**

**Purpose**: Semantic search and similarity matching for enhanced research

**Vector Strategy**:
- **Embedding Model**: BGE-small-en-v1.5 (384 dimensions)
- **Collection Structure**: Organized by topic domains
- **Indexing**: HNSW for fast approximate search
- **Metadata**: Rich filtering capabilities

**Use Cases**:
- **Semantic Search**: Find related content across reports
- **Knowledge Base**: Build organizational memory
- **Personalization**: Tailor results to user interests
- **Analytics**: Content clustering and trend analysis

### **Data Flow Patterns**

#### **Read Path Optimization**

```
User Query → Redis Check → Cache Hit? → Return Cached Result
                    ↓
                Cache Miss → Check PostgreSQL Limits → Execute Pipeline
                                        ↓
                            Store in Redis → Return New Result
```

#### **Write Path Efficiency**

```
Pipeline Complete → Store in Redis (immediate)
                         ↓
                  Queue PostgreSQL Write (async)
                         ↓
                  Optional Qdrant Embedding (background)
```

### **Data Consistency Strategy**

#### **Eventual Consistency Model**
- **Critical Path**: Redis for immediate user experience
- **Analytics Path**: PostgreSQL for business intelligence
- **Background Processing**: Qdrant for enhanced features

#### **Conflict Resolution**
- **Source of Truth**: PostgreSQL for subscription status
- **Cache Invalidation**: Event-driven Redis updates
- **Reconciliation**: Daily batch jobs for data alignment

---

## ⚡ Performance Architecture

### **Async Processing Foundation**

#### **AsyncIO Architecture**

**Event Loop Design**:
- **Single-threaded**: Eliminates race conditions
- **Non-blocking I/O**: Maximum concurrent operation support
- **Task Queuing**: Efficient work distribution
- **Error Isolation**: Failures don't cascade

**Concurrency Patterns**:
```python
# Parallel paragraph processing
tasks = [research_paragraph(p) for p in paragraphs]
results = await asyncio.gather(*tasks, return_exceptions=True)

# Concurrent search operations
search_tasks = [exa_search(query) for query in refined_queries]
search_results = await asyncio.gather(*search_tasks)
```

#### **Resource Management**

##### **Connection Pooling**
- **Database Connections**: Async connection pools
- **HTTP Clients**: Persistent connections with keep-alive
- **Redis Connections**: Connection pool per worker
- **Rate Limiting**: Per-service connection limits

##### **Memory Management**
- **Streaming Responses**: Minimize memory footprint
- **Garbage Collection**: Explicit cleanup of large objects
- **Buffer Management**: Bounded queues and buffers
- **Memory Monitoring**: Track usage patterns and optimize

### **Caching Strategy Deep Dive**

#### **Multi-Level Cache Hierarchy**

##### **L1 Cache - Application Memory**
- **Scope**: Frequently accessed configuration data
- **TTL**: Application lifetime
- **Size**: 50MB max per worker
- **Benefits**: Zero latency for hot data

##### **L2 Cache - Redis Local**
- **Scope**: User-specific and session data
- **TTL**: Tier-based (24h to 7d)
- **Size**: 1GB allocated per tier
- **Benefits**: Sub-millisecond access

##### **L3 Cache - Redis Distributed**
- **Scope**: Shared data across all users
- **TTL**: Content-type specific
- **Size**: 10GB+ cluster capacity
- **Benefits**: Shared efficiency gains

#### **Cache Key Design Principles**

##### **Hierarchical Namespace**
```
# Report cache
report:tier:sha256(user_id:topic:timestamp)

# Search cache  
search:sha256(query):version:timestamp

# User session
session:user_id:device_id:timestamp
```

##### **Cache Invalidation Strategy**
- **TTL-Based**: Automatic expiration for most data
- **Event-Driven**: Immediate invalidation on updates
- **Version-Based**: Graceful cache evolution
- **Manual**: Admin tools for targeted invalidation

### **Performance Monitoring**

#### **Key Metrics Tracking**

##### **Response Time Metrics**
- **Pipeline Duration**: End-to-end research time
- **Cache Hit Rates**: Effectiveness of caching strategy
- **API Response Times**: Per-endpoint performance
- **Database Query Times**: Identify bottlenecks

##### **Throughput Metrics**
- **Requests per Second**: Overall system capacity
- **Concurrent Users**: Active user handling
- **Queue Depths**: Backpressure indicators
- **Error Rates**: System reliability metrics

#### **Auto-Scaling Triggers**

##### **Horizontal Scaling**
- **CPU Utilization**: >70% for 5 minutes
- **Memory Usage**: >80% sustained
- **Queue Depth**: >100 pending requests
- **Response Time**: >95th percentile degradation

##### **Vertical Scaling**
- **Memory Pressure**: Automatic Redis scaling
- **Database Load**: Read replica provisioning
- **Cache Overflow**: Dynamic memory allocation

---

## Security & Reliability

### **Authentication & Authorization**

#### **JWT-Based Security Model**

##### **Token Structure**
```json
{
  "sub": "user_id",
  "tier": "pro",
  "exp": "expiration_timestamp",
  "iat": "issued_at",
  "permissions": ["query", "admin"]
}
```

##### **Security Features**
- **Asymmetric Signing**: RSA-256 for token integrity
- **Short Expiration**: 1-hour tokens with refresh
- **Scope Limitation**: Minimal permission grants
- **Revocation**: Blacklist support for compromised tokens

#### **Rate Limiting Architecture**

##### **Multi-Tier Rate Limiting**
- **Global**: 1000 requests/minute per IP
- **User**: Tier-based daily limits
- **API Key**: Service-specific limits
- **Endpoint**: Operation-specific restrictions

##### **Implementation Strategy**
```python
# Token bucket algorithm
bucket = TokenBucket(
    capacity=tier_limits[user.tier]["queries_per_day"],
    refill_rate=1/86400,  # 1 per day
    redis_key=f"rate_limit:{user.id}"
)
```

### **Data Protection**

#### **Encryption Strategy**

##### **Data at Rest**
- **Database**: AES-256 encryption for sensitive fields
- **Cache**: Encrypted Redis with TLS
- **Files**: Encrypted temporary storage
- **Backups**: Encrypted backup storage

##### **Data in Transit**
- **API Communication**: TLS 1.3 mandatory
- **Internal Services**: mTLS for service mesh
- **Database Connections**: Encrypted connections only
- **Cache Protocol**: Redis AUTH and TLS

##### **PCI Compliance**
- **No Card Storage**: Stripe handles all payment data
- **Token Security**: Payment tokens only
- **Audit Logging**: Complete payment audit trail
- **Secure Communication**: PCI-DSS compliant architecture

### **Error Handling & Recovery**

#### **Graceful Degradation Strategy**

##### **Service Failure Scenarios**
```
OpenRouter Down → Use cached responses or alternative models
Exa.ai Failure → Fall back to cached search results
Redis Outage → Direct database operation (slower)
Database Issues → Read-only mode with cache serving
```

##### **Partial Failure Handling**
- **Research Failures**: Continue with available sections
- **Model Failures**: Automatic fallback to secondary models
- **Search Failures**: Use cached or alternative sources
- **Payment Failures**: Grace period before service restriction

#### **Monitoring & Alerting**

##### **Health Check Endpoints**
```
/health → Overall system status
/health/detailed → Component-specific status
/health/database → Database connectivity
/health/cache → Redis cluster status
/health/external → Third-party service status
```

##### **Alerting Strategy**
- **Error Rate**: >5% error rate for 2 minutes
- **Response Time**: >95th percentile degradation
- **Service Availability**: Any component down
- **Resource Usage**: Memory/CPU thresholds
- **Business Metrics**: Conversion rate drops

### **Disaster Recovery**

#### **Backup Strategy**

##### **Database Backups**
- **Frequency**: Continuous WAL shipping + daily full backups
- **Retention**: 30 days point-in-time recovery
- **Testing**: Monthly restore verification
- **Geographic**: Multi-region backup storage

##### **Cache Recovery**
- **Redis Persistence**: RDB snapshots every 6 hours
- **Cache Warming**: Automated popular content preloading
- **Graceful Startup**: Progressive cache rebuilding
- **Monitoring**: Cache hit rate tracking during recovery

#### **Business Continuity**

##### **RTO/RPO Targets**
- **Recovery Time Objective**: 15 minutes for critical services
- **Recovery Point Objective**: Maximum 1 hour data loss
- **Service Degradation**: Acceptable during recovery period
- **Communication**: Automated status page updates

---

## Deployment & Operations

### **Containerized Deployment Strategy**

#### **Docker Architecture**

##### **Multi-Container Setup**
```yaml
services:
  api:          # FastAPI application
  redis:        # Cache and session storage
  postgres:     # Primary database
  qdrant:       # Vector search database
  nginx:        # Load balancer and SSL termination
  monitoring:   # Prometheus and Grafana
```

##### **Container Optimization**
- **Multi-stage Builds**: Minimize image size and attack surface
- **Distroless Images**: Security-hardened base images
- **Resource Limits**: CPU and memory constraints per container
- **Health Checks**: Container-level health monitoring

#### **Orchestration Strategy**

##### **Kubernetes Deployment**
```yaml
# API deployment with auto-scaling
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexa-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nexa-api
  template:
    spec:
      containers:
      - name: api
        image: nexa/api:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

##### **Service Mesh Integration**
- **Istio**: Traffic management and security policies
- **mTLS**: Automatic service-to-service encryption
- **Circuit Breakers**: Fault tolerance patterns
- **Observability**: Distributed tracing and metrics

### **Infrastructure Requirements**

#### **Production Environment Specifications**

##### **Compute Resources**
- **API Servers**: 4 vCPU, 8GB RAM per instance (minimum 3 instances)
- **Database**: 8 vCPU, 32GB RAM with SSD storage
- **Redis Cluster**: 6 nodes, 4GB RAM each
- **Load Balancer**: 2 vCPU, 4GB RAM with high availability

##### **Storage Requirements**
- **Database Storage**: 500GB SSD with 3000 IOPS minimum
- **Redis Memory**: 24GB total cluster memory
- **Backup Storage**: 2TB with 99.999999999% durability
- **Log Storage**: 100GB with 30-day retention

#### **Network Architecture**

##### **Security Zones**
```
Internet → WAF → Load Balancer → API Gateway → Application Services
                                      ↓
                              Internal Network → Databases
```

##### **Traffic Flow**
- **Ingress**: HTTPS only with TLS 1.3
- **Internal**: Private subnets with NAT gateways
- **Database**: Isolated subnet with no internet access
- **Egress**: Controlled outbound for API calls

### **Operational Features**

#### **Administrative Tools**

##### **CLI Management Interface**
```bash
# User management
nexa-admin user create --email user@example.com --tier pro
nexa-admin user upgrade --user-id 123 --tier custom
nexa-admin user ban --user-id 456 --reason abuse

# System maintenance
nexa-admin cache flush --pattern "report:*"
nexa-admin cache stats --detailed
nexa-admin models switch --type reasoner --model qwen-72b

# Analytics and reporting
nexa-admin analytics daily --date 2024-01-15
nexa-admin analytics usage --tier pro --month january
nexa-admin analytics performance --service all
```

##### **Web-Based Admin Dashboard**
- **User Management**: Search, view, and modify user accounts
- **System Monitoring**: Real-time metrics and alerts
- **Configuration**: Model routing and tier limit adjustments
- **Analytics**: Usage patterns and business metrics
- **Support Tools**: Query debugging and error investigation

#### **Monitoring & Observability**

##### **Metrics Collection**

**Application Metrics**:
```
# Request metrics
http_requests_total{method, endpoint, status}
http_request_duration_seconds{method, endpoint}

# Business metrics  
research_queries_total{tier, status}
research_duration_seconds{tier}
cache_hit_rate{cache_type}

# System metrics
memory_usage_bytes{service}
cpu_usage_percent{service}
database_connections{pool}
```

**Custom Dashboards**:
- **Operational Dashboard**: System health and performance
- **Business Dashboard**: Revenue, usage, and conversion metrics
- **User Dashboard**: Individual user analytics and support
- **Developer Dashboard**: API performance and error tracking

##### **Logging Strategy**

**Structured Logging Format**:
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "research-engine",
  "correlation_id": "req-123456",
  "user_id": "user-789",
  "event": "research_completed",
  "duration_ms": 15432,
  "metadata": {
    "topic": "AI healthcare",
    "word_count": 2847,
    "sources": 12
  }
}
```

**Log Aggregation**:
- **ELK Stack**: Elasticsearch, Logstash, Kibana for log analysis
- **Retention**: 90 days for application logs, 1 year for audit logs
- **Alerting**: Automated alerts on error patterns and anomalies
- **Search**: Full-text search across all application logs

### **Performance Optimization**

#### **Auto-Scaling Configuration**

##### **Horizontal Pod Autoscaler (HPA)**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nexa-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nexa-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

##### **Vertical Pod Autoscaler (VPA)**
- **Memory Optimization**: Automatic memory allocation adjustment
- **CPU Right-sizing**: Optimal CPU resource allocation
- **Cost Optimization**: Minimize over-provisioning
- **Performance Tuning**: Continuous resource optimization

#### **Database Optimization**

##### **Query Performance**
```sql
-- Optimized indexes for common queries
CREATE INDEX CONCURRENTLY idx_queries_user_date 
ON queries (user_id, created_at DESC);

CREATE INDEX CONCURRENTLY idx_subscriptions_user_status 
ON subscriptions (user_id, status) 
WHERE status = 'active';

-- Partitioning strategy for large tables
CREATE TABLE queries_2024_01 PARTITION OF queries
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

##### **Connection Optimization**
- **PgBouncer**: Connection pooling and management
- **Read Replicas**: Separate read and write workloads
- **Query Caching**: Frequently accessed data caching
- **Slow Query Monitoring**: Identify and optimize bottlenecks

### **Security Operations**

#### **Security Monitoring**

##### **Threat Detection**
- **Rate Limiting Violations**: Automated IP blocking
- **Authentication Failures**: Account lockout mechanisms  
- **Unusual Usage Patterns**: Machine learning anomaly detection
- **API Abuse**: Pattern recognition and blocking

##### **Security Scanning**
- **Container Scanning**: Vulnerability assessment in CI/CD
- **Dependency Scanning**: Third-party library security checks
- **Infrastructure Scanning**: Cloud security posture management
- **Penetration Testing**: Quarterly security assessments

#### **Incident Response**

##### **Response Procedures**
1. **Detection**: Automated alerting and monitoring
2. **Assessment**: Rapid impact and scope evaluation
3. **Containment**: Immediate threat isolation
4. **Eradication**: Root cause elimination
5. **Recovery**: Service restoration and validation
6. **Lessons Learned**: Post-incident analysis and improvement

##### **Communication Plan**
- **Internal**: Immediate team notifications via Slack/PagerDuty
- **External**: Status page updates for customer communication
- **Regulatory**: Compliance notifications when required
- **Documentation**: Detailed incident reports and timelines

### **Cost Optimization**

#### **Resource Efficiency**

##### **Compute Optimization**
- **Right-sizing**: Regular resource utilization analysis
- **Spot Instances**: Non-critical workloads on spot instances
- **Reserved Capacity**: Long-term commitments for predictable workloads
- **Auto-scaling**: Dynamic scaling based on demand

##### **API Cost Management**
- **Model Selection**: Cost-performance optimization for AI models
- **Caching Strategy**: Minimize API calls through intelligent caching
- **Batching**: Combine requests where possible
- **Usage Monitoring**: Track and optimize API consumption

#### **Financial Operations**

##### **Cost Tracking**
```
# Cost allocation by service
monthly_costs:
  - openrouter_api: $1,200
  - exa_search: $800  
  - infrastructure: $2,000
  - stripe_fees: $150
  - monitoring: $100

# Revenue tracking
monthly_revenue:
  - pro_subscriptions: $5,800 (200 users × $29)
  - custom_subscriptions: $12,000 (4 enterprises)
  - total: $17,800
```

##### **Profitability Analysis**
- **Unit Economics**: Cost per query by tier
- **LTV/CAC Ratio**: Customer lifetime value vs acquisition cost
- **Gross Margins**: Revenue minus direct costs
- **Scalability Metrics**: Cost scaling vs revenue scaling

#### **Quality Metrics**

| Metric                | Target              | Measurement              |
|-----------------------|---------------------|--------------------------|
| **Report Accuracy**   | > 95%               | Fact-checking validation |
| **Source Quality**    | > 90% authoritative | Domain authority scoring |
| **Cache Hit Rate**    | > 70%               | Redis analytics          |
| **User Satisfaction** | > 4.5/5             | Post-query surveys       |

### **Capacity Planning**

#### **Growth Projections**

##### **Year 1 Targets**
- **Total Users**: 10,000 (8,000 free, 1,800 pro, 200 custom)
- **Daily Queries**: 25,000 average, 50,000 peak
- **Revenue Target**: $65,000 MRR
- **Infrastructure Cost**: < 30% of revenue

##### **Scaling Milestones**
- **100K users**: Migrate to microservices architecture
- **1M queries/day**: Implement distributed caching
- **$1M ARR**: Add dedicated customer success team
- **Global expansion**: Multi-region deployment

### **Business Expansion**

#### **Market Expansion**
- **Vertical Markets**: Healthcare, Legal, Finance, Education
- **Geographic Markets**: EU, APAC, Latin America
- **Customer Segments**: Enterprise, Government, Academic
- **Channel Partners**: System integrators, consultants

#### **Product Extensions**
- **Research Assistant**: Interactive research conversations
- **Knowledge Base**: Organizational memory and search
- **Competitive Intelligence**: Automated market research
- **Compliance Monitoring**: Regulatory change tracking

---

### **Development Resources**
- **SDK Libraries**: Python, JavaScript, Go, Java
- **Postman Collection**: Pre-configured API requests
- **Docker Images**: Official container images

---

*This architecture guide serves as a comprehensive reference for understanding, deploying, and operating the Nexa Research Agent platform. For the most current information, please refer to the official documentation and repository.*

**Last Updated**: January 2024  
**Version**: 1.0.0  
**Maintainers**: Nexa Engineering Team
