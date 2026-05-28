# 🎓 Interview Prep Supplement

> **From Coding to Hiring Manager**
>
> Complete guide to technical and behavioral interview preparation for Python developers. Covers coding problems, system design, behavioral questions, and company-specific strategies.

---

## Table of Contents

1. [Interview Overview](#interview-overview)
2. [Coding Interview Fundamentals](#coding-interview-fundamentals)
3. [50 Essential Coding Problems](#50-essential-coding-problems)
4. [System Design Basics](#system-design-basics)
5. [System Design Problems](#system-design-problems)
6. [Behavioral Interviews](#behavioral-interviews)
7. [STAR Method](#star-method)
8. [Common Interview Scenarios](#common-interview-scenarios)
9. [Company-Specific Preparation](#company-specific-preparation)
10. [Mock Interview Checklist](#mock-interview-checklist)
11. [Interview Day Guide](#interview-day-guide)
12. [Negotiation Tips](#negotiation-tips)

---

## Interview Overview

### Types of Technical Interviews

| Type | Duration | Focus | Difficulty |
|------|----------|-------|-----------|
| **Phone Screen** | 30-45 min | Coding basics, communication | Medium |
| **Online Assessment** | 60-90 min | 1-2 coding problems, timed | Medium-Hard |
| **Coding Round** | 45-60 min | 1-2 problems, live interview | Hard |
| **System Design** | 45-60 min | Architecture, tradeoffs | Hard |
| **Behavioral** | 30-45 min | Stories, culture fit | Medium |
| **Hiring Manager** | 30-45 min | Role fit, team dynamics | Easy-Medium |
| **Final Round** | Varies | All aspects combined | Varies |

### Interview Process Timeline

```
Application → Phone Screen (1-2 weeks)
    ↓
Online Assessment or Coding Round (1-2 weeks)
    ↓
System Design + Behavioral (1-2 weeks)
    ↓
Final Round / Hiring Manager (1-2 weeks)
    ↓
Offer
```

---

## Coding Interview Fundamentals

### Time Management

- **5-10 min**: Understand problem, ask clarifying questions
- **20-30 min**: Write solution
- **5-10 min**: Test with examples
- **5 min**: Optimize if time permits

### Approach

```
1. Listen carefully to the problem
2. Ask clarifying questions
3. Think aloud - explain your approach
4. Write pseudocode first
5. Code slowly and carefully
6. Test with multiple examples
7. Optimize (time/space) if time permits
8. Discuss tradeoffs
```

### Common Mistakes to Avoid

❌ Not asking clarifying questions
❌ Jumping to code without planning
❌ Writing messy, unreadable code
❌ Ignoring edge cases
❌ Not testing your code
❌ Being defensive about feedback
❌ Not thinking aloud
❌ Over-complicating solution

### What Interviewers Look For

✅ Problem-solving approach
✅ Communication & clarity
✅ Code quality & readability
✅ Testing & edge case handling
✅ Time/space complexity awareness
✅ Ability to optimize
✅ Handling feedback gracefully

---

## 50 Essential Coding Problems

### Arrays & Strings (8 problems)

1. **Two Sum**
   - Given array, find two numbers that sum to target
   - Difficulty: Easy | Time: O(n) | Space: O(n)

2. **Median of Two Sorted Arrays**
   - Find median of two sorted arrays
   - Difficulty: Hard | Time: O(log(min(m,n))) | Space: O(1)

3. **Longest Substring Without Repeating Characters**
   - Find length of longest substring with unique chars
   - Difficulty: Medium | Time: O(n) | Space: O(min(m,n))

4. **Container With Most Water**
   - Find two lines with max area
   - Difficulty: Medium | Time: O(n) | Space: O(1)

5. **Trapping Rain Water**
   - Calculate trapped water in elevation map
   - Difficulty: Hard | Time: O(n) | Space: O(1)

6. **3Sum**
   - Find all unique triplets that sum to zero
   - Difficulty: Medium | Time: O(n²) | Space: O(1)

7. **Merge Sorted Array**
   - Merge two sorted arrays in-place
   - Difficulty: Easy | Time: O(m+n) | Space: O(1)

8. **Rotate Array**
   - Rotate array by k positions
   - Difficulty: Medium | Time: O(n) | Space: O(1)

### Linked Lists (6 problems)

9. **Reverse Linked List**
   - Reverse linked list iteratively
   - Difficulty: Easy | Time: O(n) | Space: O(1)

10. **Linked List Cycle Detection**
    - Detect if linked list has cycle
    - Difficulty: Medium | Time: O(n) | Space: O(1)

11. **Merge Two Sorted Lists**
    - Merge two sorted linked lists
    - Difficulty: Easy | Time: O(n+m) | Space: O(1)

12. **Reorder List**
    - Reorder list as L₀ → Lₙ → L₁ → Lₙ₋₁ → ...
    - Difficulty: Medium | Time: O(n) | Space: O(1)

13. **Intersection of Two Linked Lists**
    - Find intersection node of two lists
    - Difficulty: Easy | Time: O(n+m) | Space: O(1)

14. **Copy List with Random Pointer**
    - Deep copy linked list with random pointer
    - Difficulty: Medium | Time: O(n) | Space: O(n)

### Trees & Graphs (10 problems)

15. **Binary Tree Maximum Path Sum**
    - Find maximum path sum in binary tree
    - Difficulty: Hard | Time: O(n) | Space: O(h)

16. **Lowest Common Ancestor**
    - Find LCA of two nodes in binary tree
    - Difficulty: Medium | Time: O(n) | Space: O(h)

17. **Serialize and Deserialize Binary Tree**
    - Convert tree to string and back
    - Difficulty: Hard | Time: O(n) | Space: O(n)

18. **Word Ladder**
    - Find shortest path to transform word
    - Difficulty: Medium | Time: O(n*l) | Space: O(n)

19. **Number of Islands**
    - Count islands in grid
    - Difficulty: Medium | Time: O(m*n) | Space: O(m*n)

20. **Topological Sort**
    - Order nodes with dependencies
    - Difficulty: Medium | Time: O(V+E) | Space: O(V)

21. **Course Schedule II**
    - Determine course order (detect cycle)
    - Difficulty: Medium | Time: O(V+E) | Space: O(V)

22. **Clone Graph**
    - Deep copy undirected graph
    - Difficulty: Medium | Time: O(V+E) | Space: O(V)

23. **Reconstruct Itinerary**
    - Build path visiting each edge once
    - Difficulty: Medium | Time: O(E log E) | Space: O(V+E)

24. **Binary Tree Level Order Traversal**
    - Traverse tree level by level
    - Difficulty: Medium | Time: O(n) | Space: O(w)

### Dynamic Programming (8 problems)

25. **Longest Increasing Subsequence**
    - Find length of LIS
    - Difficulty: Medium | Time: O(n²) or O(n log n) | Space: O(n)

26. **Coin Change**
    - Minimum coins for amount
    - Difficulty: Medium | Time: O(n*m) | Space: O(n)

27. **House Robber**
    - Maximum money robbing non-adjacent houses
    - Difficulty: Medium | Time: O(n) | Space: O(1)

28. **Edit Distance**
    - Minimum operations to transform word
    - Difficulty: Medium | Time: O(m*n) | Space: O(m*n)

29. **Longest Common Subsequence**
    - Find longest common subsequence
    - Difficulty: Medium | Time: O(m*n) | Space: O(m*n)

30. **Maximum Subarray (Kadane's Algorithm)**
    - Find contiguous subarray with max sum
    - Difficulty: Easy | Time: O(n) | Space: O(1)

31. **Best Time to Buy and Sell Stock**
    - Maximum profit from buying/selling once
    - Difficulty: Easy | Time: O(n) | Space: O(1)

32. **Palindrome Partitioning**
    - All ways to partition string into palindromes
    - Difficulty: Medium | Time: O(n*2ⁿ) | Space: O(n)

### Sorting & Searching (6 problems)

33. **Sort Colors**
    - Sort array with 0s, 1s, 2s (in-place)
    - Difficulty: Medium | Time: O(n) | Space: O(1)

34. **Search in Rotated Sorted Array**
    - Binary search in rotated array
    - Difficulty: Medium | Time: O(log n) | Space: O(1)

35. **Kth Largest Element**
    - Find kth largest element
    - Difficulty: Medium | Time: O(n) | Space: O(k)

36. **Merge Intervals**
    - Merge overlapping intervals
    - Difficulty: Medium | Time: O(n log n) | Space: O(n)

37. **Meeting Rooms II**
    - Minimum conference rooms needed
    - Difficulty: Medium | Time: O(n log n) | Space: O(n)

38. **Skyline Problem**
    - Compute skyline silhouette
    - Difficulty: Hard | Time: O(n log n) | Space: O(n)

### Backtracking (4 problems)

39. **N-Queens**
    - Place N queens on NxN board
    - Difficulty: Hard | Time: O(N!) | Space: O(N)

40. **Word Search**
    - Find word in grid (DFS)
    - Difficulty: Medium | Time: O(n*m*4ᶠ) | Space: O(f)

41. **Combination Sum**
    - Find combinations that sum to target
    - Difficulty: Medium | Time: O(n^(t/m)) | Space: O(t/m)

42. **Permutations**
    - Generate all permutations
    - Difficulty: Medium | Time: O(n!) | Space: O(n)

### Miscellaneous (8 problems)

43. **LRU Cache**
    - Implement least-recently-used cache
    - Difficulty: Medium | Time: O(1) | Space: O(capacity)

44. **Median of Data Stream**
    - Find median of stream of numbers
    - Difficulty: Hard | Time: O(log n) | Space: O(n)

45. **Design Twitter**
    - Design Twitter system
    - Difficulty: Medium | Time: Varies | Space: O(n)

46. **Regular Expression Matching**
    - Pattern matching with '.' and '*'
    - Difficulty: Hard | Time: O(m*n) | Space: O(m*n)

47. **Wildcard Matching**
    - Pattern matching with '?' and '*'
    - Difficulty: Hard | Time: O(m*n) | Space: O(m*n)

48. **Integer to Roman**
    - Convert integer to Roman numerals
    - Difficulty: Medium | Time: O(1) | Space: O(1)

49. **Pow(x, n)**
    - Calculate x^n efficiently
    - Difficulty: Medium | Time: O(log n) | Space: O(1)

50. **Majority Element**
    - Find element appearing > n/2 times
    - Difficulty: Easy | Time: O(n) | Space: O(1)

### Practice Strategy

```
Week 1-2: Arrays & Strings (start easy, progress to hard)
Week 3-4: Linked Lists & Trees
Week 5-6: Dynamic Programming & Backtracking
Week 7-8: Review hard problems & optimize
```

### Resources

- **LeetCode** - 2500+ problems by difficulty
- **HackerRank** - Tutorials + practice
- **GeeksforGeeks** - Detailed solutions
- **Cracking the Coding Interview** - Book with 189 problems

---

## System Design Basics

### Key Concepts

#### Scalability

**Vertical Scaling (Scale Up)**
- Add more resources to single server
- Easy to implement
- Limited by hardware
- Example: More CPU, RAM

**Horizontal Scaling (Scale Out)**
- Add more servers
- More complex (coordination needed)
- Unlimited scaling
- Better for distributed systems

#### Load Balancing

```
Clients → Load Balancer → Multiple Servers
         (distributes traffic)
```

**Algorithms:**
- Round-robin
- Least connections
- IP hash
- Weighted distribution

#### Caching

```
Client → Cache → Database
         (fast, temporary storage)
```

**Cache Patterns:**
- Cache-aside (lazy loading)
- Write-through
- Write-behind

**Tools:** Redis, Memcached

#### Database Scaling

**Replication**
- Master-slave
- High availability
- Read scaling

**Sharding**
- Partition data
- Write scaling
- More complex (routing, rebalancing)

#### Message Queues

```
Producer → Message Queue → Consumer
          (async processing)
```

**Benefits:**
- Decoupling
- Load leveling
- Reliability

**Tools:** RabbitMQ, Kafka, SQS

#### API Design

```
REST: GET /users/123
      POST /users
      PUT /users/123
      DELETE /users/123
```

---

## System Design Problems

### E-commerce: Design Amazon

**Requirements:**
- Users can browse products
- View details, add to cart
- Place orders, make payments
- Track order status

**Architecture:**

```
Clients (Web, Mobile)
    ↓
API Gateway + Load Balancer
    ↓
Microservices:
├── Product Service (search, browse)
├── Cart Service (add, remove, checkout)
├── Order Service (create, track)
├── Payment Service (process payments)
├── User Service (auth, profile)
    ↓
Cache Layer (Redis)
    ↓
Databases (read replicas, sharded)
    ↓
Message Queue (events)
```

**Database Schema:**
- Products table (searchable, indexed)
- Users table (auth)
- Orders table (sharded by user_id)
- OrderItems table (order details)

**Optimization:**
- Cache product catalog
- Shard orders by user_id
- Async payment processing
- CDN for images

---

### Real-Time: Design Uber

**Requirements:**
- Users request rides
- Drivers see requests
- Real-time location tracking
- Match drivers to riders

**Architecture:**

```
Clients (Web, Mobile)
    ↓
WebSocket Server (real-time updates)
    ↓
Location Service (tracking)
├── Geospatial indexing (quadtree)
├── Find nearby drivers
    ↓
Matching Service
├── Match optimization
├── Price calculation
    ↓
Message Queue
├── Ride events
├── Payment processing
    ↓
Databases + Cache
```

**Key Challenges:**
- Real-time location updates (100s of locations/sec)
- Geospatial querying (find nearby drivers)
- High availability & consistency tradeoff
- Payment at scale

**Solutions:**
- WebSockets for real-time
- Geohash/Quadtree for location
- Eventually consistent
- Event sourcing for audit

---

### Messaging: Design Twitter

**Requirements:**
- Users post tweets
- Follow other users
- View feed
- Like tweets

**Architecture:**

```
Clients
    ↓
API Services (REST)
    ├── Timeline Service (generate feed)
    ├── Tweet Service (post tweet)
    ├── Follow Service (manage follows)
    ├── Like Service
    ↓
Message Queue
├── Tweet published event
├── User followed event
├── Like event
    ↓
Feed Generation Service
├── Generate personalized feed
├── Cache user timelines
    ↓
Databases
├── Tweets (sharded by tweet_id)
├── Users
├── Follows
├── Likes
    ↓
Cache (Redis)
├── User timelines (hot)
├── Friend lists
```

**Optimization:**
- Pre-compute feeds (push model)
- Or lazy compute (pull model)
- Cache hot users' timelines
- Asynchronous like processing

---

### Video Streaming: Design Netflix

**Requirements:**
- Upload videos
- Stream videos
- View recommendations
- Track watch history

**Key Challenges:**
- Huge data (100s TB)
- Different network speeds
- Geographically distributed users
- Real-time encoding

**Architecture:**

```
Content Upload
    ↓
Video Encoding (multiple qualities)
    ├── H.264, VP9, H.265
    ├── 480p, 720p, 1080p, 4K
    ↓
CDN (Content Delivery Network)
├── Geographically distributed
├── Cache popular content
    ↓
Streaming Server
├── Adaptive bitrate streaming
├── User bandwidth detection
    ↓
Database
├── Video metadata
├── Watch history
├── User preferences
    ↓
ML Service
├── Recommendations
```

**Optimization:**
- CDN for geographic distribution
- Adaptive bitrate (auto quality)
- Pre-buffer next segment
- Regional caching

---

### Chat: Design Facebook Messenger

**Requirements:**
- Send/receive messages
- Real-time notifications
- Group chats
- Message history

**Architecture:**

```
Clients (Web, Mobile)
    ↓
Message Service (REST/WebSocket)
├── Send message
├── Get conversation
    ↓
WebSocket Server (real-time)
├── Live message delivery
├── Typing indicators
├── Read receipts
    ↓
Message Queue
├── Async delivery
├── Guarantee delivery
    ↓
Database (sharded)
├── Messages (sharded by conversation_id)
├── Conversations
├── Users
    ↓
Cache (Redis)
├── Recent conversations
├── Unread count
├── User online status
```

**Optimization:**
- WebSockets for real-time
- Message queue for reliability
- Cache hot conversations
- Shard by conversation
- Lazy load message history

---

## Behavioral Interviews

### Why Behavioral Questions?

- Assess communication skills
- Evaluate teamwork & collaboration
- Understand problem-solving style
- Check culture fit
- Learn from past experiences

### Common Categories

| Category | Focus | Example |
|----------|-------|---------|
| **Teamwork** | Collaboration skills | "Describe a time you worked with difficult person" |
| **Leadership** | Taking initiative | "Tell me about a project you led" |
| **Conflict** | Resolution skills | "How do you handle disagreement with manager?" |
| **Failure** | Learning from mistakes | "Describe a failure and what you learned" |
| **Impact** | Results & metrics | "Give example of your biggest accomplishment" |

---

## STAR Method

### Structure

**Situation**: Set the context (2-3 sentences)
**Task**: Your role and challenge (1-2 sentences)
**Action**: What you did (3-5 sentences)
**Result**: Outcomes and metrics (2-3 sentences)

### Example

**Question:** "Tell me about a time you resolved a conflict with a colleague."

**Answer:**

**Situation:** I was working on a web application project with another developer who had a different approach to database optimization.

**Task:** We disagreed on using indexes vs. caching. He wanted indexes, I advocated for caching. The disagreement was slowing our progress.

**Action:** I suggested we both present our approaches to the team. I created a benchmark showing pros/cons of each method. We discussed the trade-offs openly. I listened to his concerns about cache invalidation complexity. We decided to use both: indexes for exact matches, cache for frequent queries.

**Result:** Implementation finished on time. Performance improved 40% over baseline. Team learned both techniques. We built better working relationship based on data-driven decisions, not emotions.

### Tips

✅ Use specific metrics (numbers, percentages)
✅ Show your growth and learning
✅ Focus on "I" not "we" (your contribution)
✅ Practice out loud to improve delivery
✅ Keep to 2-3 minutes per story
✅ Prepare 5-7 stories covering different angles

---

## Common Interview Scenarios

### Scenario 1: "Walk me through your approach to this system design problem"

**Good approach:**
1. Ask clarifying questions (scale, regions, features)
2. Define requirements (functional & non-functional)
3. Draw high-level architecture
4. Deep dive into components
5. Discuss bottlenecks & solutions
6. Talk tradeoffs
7. Answer follow-up questions

### Scenario 2: "Why did you leave your last job?"

**Good responses:**
- "Looking for bigger challenges"
- "Want to work with specific technology"
- "Company was moving in different direction"
- "Personal growth opportunity"

**Avoid:**
- Blaming manager or company
- Complaining
- Vague answers
- Appearing job-hopping

### Scenario 3: "Tell me about your biggest failure"

**Structure:**
1. Pick real failure (medium severity)
2. Explain what happened
3. Take ownership (no excuses)
4. Describe what you learned
5. Show how you changed behavior
6. Explain positive outcome

### Scenario 4: "You disagree with your manager's decision. What do you do?"

**Good approach:**
1. Clarify you understand their perspective
2. Present your data/reasoning calmly
3. Ask questions to understand their thinking
4. Listen to their rationale
5. Offer to try their way with clear metrics to measure
6. If still disagreeing, you implement their decision professionally
7. Follow up with results

### Scenario 5: "What's your biggest weakness?"

**Strategy:**
1. Pick real weakness (relevant to role)
2. Show self-awareness
3. Describe how you're improving
4. Provide evidence of improvement
5. Frame as learning opportunity

**Example:**
"I used to struggle with public speaking. I found it anxiety-inducing. I joined Toastmasters, gave talks at local meetups, and presented quarterly at my company. Now I'm much more comfortable and actually enjoy sharing ideas."

---

## Company-Specific Preparation

### FAANG Preparation

#### Facebook (Meta)

**Focus Areas:**
- Coding: Medium to Hard problems
- System Design: Focus on scale, real-time
- Behavioral: Teamwork, impact

**Tips:**
- Prepare for multiple interviews on same day
- Meta values "building fast"
- Technical depth in data structures
- Examples: Design News Feed, Messenger

#### Apple

**Focus Areas:**
- Product thinking
- Details & polish
- User experience

**Tips:**
- Ask thoughtful questions
- Discuss trade-offs
- Show curiosity about products
- Focus on quality & reliability

#### Amazon

**Focus Areas:**
- Customer obsession
- Operational excellence
- Leadership principles

**Tips:**
- Align answers with 14 leadership principles
- Quantify impact with metrics
- Show cost-consciousness
- Example: Design Amazon.com catalog

#### Netflix

**Focus Areas:**
- Scalability at extreme levels
- Distributed systems
- Critical thinking

**Tips:**
- Be ready for very hard system design
- Discuss edge cases
- Show experience with large systems
- Example: Design video streaming service

#### Google

**Focus Areas:**
- Algorithms & complexity
- System design at massive scale
- Innovation

**Tips:**
- Deep technical knowledge
- Optimal solutions (not just working)
- Show problem-solving process
- Example: Design search indexing

### Startup vs. Enterprise

| Aspect | Startup | Enterprise |
|--------|---------|-----------|
| **Pace** | Fast-paced, shipping quickly | Structured, longer timelines |
| **Tech** | Latest tech, experimentation | Proven, stable tech |
| **Interview** | More practical, creative | Formal, process-focused |
| **Questions** | "Can you build X?" | "Can you optimize Y?" |
| **Evaluation** | Full-stack abilities | Deep specialization |

### Preparation by Role

#### Software Engineer

- Focus: Algorithms, OOP, design patterns
- Projects: Build multiple features end-to-end
- Study: System design + coding

#### Backend Engineer

- Focus: Databases, APIs, scale
- Projects: API design, data modeling
- Study: System design, databases

#### Frontend Engineer

- Focus: UI/UX, performance, browser APIs
- Projects: Component design, state management
- Study: JavaScript, CSS, design systems

#### DevOps/Infrastructure

- Focus: Deployment, scaling, reliability
- Projects: Infrastructure as code, CI/CD
- Study: Docker, Kubernetes, cloud platforms

---

## Mock Interview Checklist

### Before Mock Interview

- [ ] Read job description
- [ ] Research company & products
- [ ] Prepare 5-7 STAR stories
- [ ] Practice 10-15 coding problems
- [ ] Study 3-4 system design problems
- [ ] Prepare smart questions to ask
- [ ] Mock interview with friend
- [ ] Get good sleep night before

### During Coding Interview

- [ ] Listen carefully to problem
- [ ] Ask clarifying questions
- [ ] Explain approach before coding
- [ ] Write clean, readable code
- [ ] Test with examples
- [ ] Discuss time/space complexity
- [ ] Optimize if time permits
- [ ] Think aloud throughout

### During System Design

- [ ] Ask about scale & requirements
- [ ] Draw architecture diagram
- [ ] Explain each component
- [ ] Discuss tradeoffs
- [ ] Address bottlenecks
- [ ] Show you know alternatives
- [ ] Deep dive on interviewer's questions
- [ ] Calculate rough numbers

### During Behavioral

- [ ] Smile, maintain eye contact
- [ ] Listen carefully
- [ ] Use STAR method
- [ ] Show enthusiasm
- [ ] Ask thoughtful questions
- [ ] Be authentic
- [ ] Give specific examples
- [ ] Keep answers to 2-3 min

### Questions to Ask Interviewer

✅ What are biggest challenges on this team?
✅ How do you measure success?
✅ What does career growth look like?
✅ What's the team structure?
✅ How often do you ship features?
✅ What's biggest pain point in codebase?
✅ How do you handle on-call?
✅ What technologies do you use?

❌ Don't ask about:
- Salary (wait for offer)
- Benefits initially
- Work hours/flexibility
- Vacation days
- Too many questions at once

---

## Interview Day Guide

### Morning of Interview

- [ ] Eat good breakfast
- [ ] Review system design notes
- [ ] Review coding problems
- [ ] Test video/audio if remote
- [ ] Close other applications
- [ ] Have water nearby
- [ ] Wear comfortable clothes
- [ ] Arrive 10 minutes early

### During Interview

**First 5 minutes:**
- Greet enthusiastically
- Make small talk
- Show genuine interest

**Problem time:**
- Listen completely before responding
- Ask for clarification
- Think aloud
- Take breaks if stuck
- Stay calm

**After solution:**
- Confirm correctness
- Optimize if possible
- Explain trade-offs

**Closing:**
- Ask thoughtful questions
- Express genuine interest
- Ask next steps

### Red Flags to Avoid

❌ Being arrogant or dismissive
❌ Criticizing previous work/company
❌ Not listening to interviewer
❌ Defensive when asked questions
❌ Rushing solutions
❌ Writing messy code
❌ Not testing your code
❌ Making up things you don't know

### Green Flags to Show

✅ Humility and learning mindset
✅ Problem-solving process
✅ Clear communication
✅ Asking clarifying questions
✅ Collaborative approach
✅ Honest about weaknesses
✅ Enthusiasm for the role
✅ Curiosity about company

---

## Negotiation Tips

### Offer Negotiation

**Before negotiating:**
- Research salary ranges (Levels.fyi, Blind)
- Know your value
- Have minimum acceptable
- Understand full compensation (bonus, stock, benefits)

**Negotiation strategy:**
1. Thank them for offer
2. Express enthusiasm about role
3. Say you'd like to discuss compensation
4. Provide your number (15-20% above market)
5. Justify with: experience, market data, impact
6. Listen to their counter
7. Negotiate other aspects if salary stuck

**What to negotiate:**
- Base salary (most important)
- Sign-on bonus
- Stock vesting
- Bonus percentage
- Remote work flexibility
- Start date
- PTO
- Professional development

**What NOT to do:**
- Don't negotiate poorly by initial conversation
- Don't sound desperate
- Don't accept first offer
- Don't compare to friends
- Don't be unreasonable

### Handling Multiple Offers

1. Get all offers in writing
2. Understand full compensation
3. Assess role fit, not just money
4. Evaluate team & manager
5. Consider growth opportunities
6. Negotiate all offers up
7. Make decision based on career goals

---

## Post-Interview

### Immediately After

- [ ] Jot down feedback/notes
- [ ] Send thank you email within 1 hour
- [ ] Highlight specific discussion points
- [ ] Reaffirm interest
- [ ] Ask timeline for decision

### If Rejected

- Ask for feedback (some companies provide)
- Ask what you could improve
- Stay positive (networking counts)
- Apply again in 1 year
- Use learnings for next interview

### If Accepted

- Negotiate offer professionally
- Ask clarifying questions
- Request any accommodations
- Prepare for first day
- Set up intro meetings
- Send gracious decline to others

---

## Timeline & Resources

### 1-Month Preparation

**Week 1-2:** Coding basics + 15 easy problems
**Week 2-3:** Medium problems + system design basics
**Week 3:** Hard problems + 2 system design problems
**Week 4:** Mock interviews + behavioral prep

### 3-Month Preparation

**Month 1:** Coding fundamentals + easy problems
**Month 2:** Medium/hard problems + system design
**Month 3:** Mock interviews + company-specific prep

### 6-Month Preparation

**Month 1-2:** Coding fundamentals + projects
**Month 3:** System design deep dive
**Month 4-5:** Mock interviews + behavioral
**Month 6:** Final prep + applications

### Resources

**Coding:**
- LeetCode Premium
- Cracking the Coding Interview book
- GeeksforGeeks tutorials
- InterviewBit

**System Design:**
- System Design Interview (Alex Xu)
- Designing Data-Intensive Applications
- Grokking System Design Interview
- YouTube: Tech Dummies, Success in Tech

**Behavioral:**
- Behavioral Interview book
- YouTube: "Behavioral interview preparation"
- Practice with friends
- Record yourself

**Interview Experience:**
- Blind app (anonymous feedback)
- LeetCode company-specific discussions
- CareerCup
- PreparedMind

---

## Final Tips

### Do's

✅ Start interview prep early
✅ Practice out loud
✅ Know your stories
✅ Ask clarifying questions
✅ Think aloud during interviews
✅ Be honest about what you don't know
✅ Enjoy the process
✅ Network regardless of outcome

### Don'ts

❌ Memorize solutions
❌ Skip behavioral prep
❌ Interview without researching company
❌ Be dishonest about skills
❌ Criticize previous employers
❌ Interview while tired
❌ Apply only to dream companies
❌ Give up after rejections

---

## Interview Success Metrics

### Good Interview = ✅

- [ ] Solved core problem correctly
- [ ] Discussed complexity & trade-offs
- [ ] Communicated clearly throughout
- [ ] Asked smart clarifying questions
- [ ] Showed genuine curiosity
- [ ] Took feedback gracefully
- [ ] Told coherent stories (behavioral)
- [ ] Asked relevant questions about role

### Great Interview = ⭐

- [ ] Optimized solution beyond first try
- [ ] Identified bottlenecks proactively
- [ ] Proposed alternatives
- [ ] Showed deep system understanding
- [ ] Demonstrated leadership
- [ ] Asked about technical direction
- [ ] Clear passion for the role
- [ ] Interviewer wants to work with you

---

## Summary Checklist

- [ ] Master 50 essential coding problems
- [ ] Understand 5 system design patterns
- [ ] Prepare 5-7 STAR stories
- [ ] Practice explaining solutions
- [ ] Research 3+ companies thoroughly
- [ ] Do 5 mock interviews minimum
- [ ] Review company-specific tips
- [ ] Prepare smart questions
- [ ] Get good sleep before interview
- [ ] Send thank you emails

---

**Last Updated:** May 2026 | **Version:** 1.0

Related resources:
- [Python Study Guide](python-study-guide.md) - Algorithm & data structures foundation
- [Quick Reference Cards](quick-reference-cards.md) - Big-O complexity, syntax
- [System Design Basics in Main Handbook](PYTHON_HANDBOOK.md#-interview-preparation)
