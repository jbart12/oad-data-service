# Quick Reference - Code Improvements

## What Changed?

Three main additions to make your code more robust:

### 1. Database Module - Now More Reliable ✅

**What's Better:**
- Connections automatically retry on failure (3 attempts)
- Bad connections are detected and closed
- Better error messages tell you exactly what went wrong
- Validates data before inserting to database

**Usage:**
```python
from database import upsert_records, DatabaseError, DatabasePool

# Check if database is healthy
if DatabasePool.health_check():
    print("✓ Database connected")

# Catch database errors specifically
try:
    upsert_records(table="players", records=data, conflict_columns=["id"])
except DatabaseError as e:
    logger.error(f"Database problem: {e}")
```

---

### 2. Configuration System - No More Hard-Coded Values ✅

**What's Better:**
- All settings in one place
- Change settings via environment variables
- Validates configuration on startup

**Usage:**
```python
from config import get_config

config = get_config()

# Access any setting
max_retries = config.api.max_retries  # 3
batch_size = config.database.batch_size  # 100
poll_interval = config.sync.poll_active_interval  # 180 seconds
```

**Environment Variables (optional):**
```bash
# .env file
DATABASE_URL=postgresql://...  # REQUIRED
PGA_TOUR_API_KEY=...           # REQUIRED

# Optional tuning
DB_POOL_MAX=20          # More connections
PGA_API_RETRIES=5       # More retries
POLL_ACTIVE_INTERVAL=120  # Poll every 2 min instead of 3
LOG_LEVEL=DEBUG         # More verbose logging
```

---

### 3. Data Validation - Prevent Bad Data ✅

**What's Better:**
- Catches invalid data before it reaches the database
- Consistent parsing across all modules
- Clear error messages

**Usage:**
```python
from services.validation import validate_money, validate_position, ValidationError

try:
    # Parse earnings safely
    earnings = validate_money("$1,234,567")  # → Decimal("1234567")

    # Parse positions correctly
    pos_str, pos_num = validate_position("T5")  # → ("T5", 5)

except ValidationError as e:
    logger.error(f"Invalid data: {e}")
```

---

## Do I Need to Change My Code?

**No!** Everything is backward compatible.

But you **should** consider:

### Optional Improvements

1. **Use configuration system:**
   ```python
   # Instead of hard-coded values
   poll_interval = 180  # ❌ old way

   # Use config
   poll_interval = get_config().sync.poll_active_interval  # ✅ better
   ```

2. **Handle DatabaseError specifically:**
   ```python
   # Instead of generic Exception
   try:
       upsert_records(...)
   except Exception as e:  # ❌ too broad
       pass

   # Catch specific errors
   try:
       upsert_records(...)
   except DatabaseError as e:  # ✅ better
       # Handle database issues
   except ValidationError as e:  # ✅ better
       # Handle invalid data
   ```

3. **Validate data from API:**
   ```python
   # Instead of hoping data is valid
   earnings = Decimal(api_data["money"])  # ❌ might fail

   # Validate first
   earnings = validate_money(api_data["money"])  # ✅ safe
   ```

---

## Quick Test

Run this to verify improvements are working:

```python
from database import DatabasePool
from config import get_config
from services.validation import validate_money

# Test 1: Health check
print("1. Database health:", "✓" if DatabasePool.health_check() else "✗")

# Test 2: Configuration
config = get_config()
print("2. Config loaded:", "✓")
print("   - API retries:", config.api.max_retries)
print("   - DB batch size:", config.database.batch_size)

# Test 3: Validation
try:
    earnings = validate_money("$1,000,000")
    print("3. Validation working:", "✓")
    print("   - Parsed:", earnings)
except Exception as e:
    print("3. Validation error:", "✗", e)
```

---

## Common Scenarios

### Scenario 1: Database Connection Fails

**Before:** App crashes
**After:** Retries 3 times, logs detailed error

```python
# Happens automatically
conn = DatabasePool.get_connection()  # Will retry if needed
```

### Scenario 2: Invalid Data from API

**Before:** Inserts invalid data or crashes
**After:** Validates and logs warning

```python
from services.validation import validate_money, ValidationError

try:
    earnings = validate_money(api_response["money"])
except ValidationError as e:
    logger.warning(f"Invalid earnings for player {player_id}: {e}")
    earnings = Decimal("0")  # Safe default
```

### Scenario 3: Need to Change Polling Interval

**Before:** Edit code, redeploy
**After:** Change environment variable, restart

```bash
# .env
POLL_ACTIVE_INTERVAL=120  # 2 minutes instead of 3
```

---

## Files to Know About

| File | What It Does |
|------|--------------|
| `CODE_REVIEW.md` | Detailed analysis of what was reviewed |
| `IMPROVEMENTS.md` | Full list of all improvements |
| `QUICK_REFERENCE.md` | This file - quick guide |
| `config.py` | Configuration system |
| `services/validation.py` | Data validation utilities |
| `database/db.py` | Enhanced database module |

---

## When Things Go Wrong

### "DatabaseError: Failed to get connection"

**Cause:** Can't connect to database
**Fix:**
1. Check `DATABASE_URL` in `.env`
2. Verify database is running
3. Check network connectivity

### "ValidationError: Invalid money value"

**Cause:** Bad data from API
**Fix:**
1. Check API response format
2. Add try/except to handle gracefully
3. Log the problematic data for investigation

### "ValueError: DB_POOL_MAX must be >= DB_POOL_MIN"

**Cause:** Invalid configuration
**Fix:** Check environment variables in `.env`

---

## Performance Impact

**Good News:** Minimal performance impact

- Connection retry: Only on failures (~1-3s delay if needed)
- Validation: Negligible (<1ms per record)
- Configuration: One-time load at startup
- Overall: Same performance, more reliable

---

## Support

- **Detailed review:** See `CODE_REVIEW.md`
- **Full improvements:** See `IMPROVEMENTS.md`
- **Configuration docs:** See inline docs in `config.py`
- **Validation docs:** See inline docs in `services/validation.py`

---

**TL;DR:**
- ✅ No breaking changes
- ✅ More reliable database operations
- ✅ Configurable settings
- ✅ Better data validation
- ✅ Clearer error messages
- ✅ Production-ready improvements
