# 📸 Understanding: Scene Images vs Text Crop Samples

## The Key Question

**"How can we have 22,726 samples from only 3,096 scene images?"**

---

## 🎯 The Answer

Each scene image contains **MULTIPLE text instances**. Each text instance is cropped separately to create individual training samples.

### Simple Example

```
Scene Image: A photo of a storefront
├─ Text 1: "COFFEE SHOP" (store name)
├─ Text 2: "OPEN 7AM-9PM" (hours)
├─ Text 3: "555-1234" (phone number)
├─ Text 4: "WIFI AVAILABLE" (sign)
└─ Text 5: "PARKING IN REAR" (sign)

Result: 1 scene image → 5 text crop samples
```

---

## 📊 Real Data from Fixed Datasets

### ArT Training Set Analysis

**Statistics:**
- Scene images: **3,096**
- Text crops: **22,726**
- **Ratio: 7.3 crops per scene**

**Distribution:**
| Crops per Scene | Number of Scenes | Percentage |
|----------------|------------------|------------|
| 1 crop | 618 scenes | 20.0% |
| 2 crops | 472 scenes | 15.2% |
| 3-4 crops | 640 scenes | 20.7% |
| 5-9 crops | 734 scenes | 23.7% |
| 10-19 crops | 426 scenes | 13.8% |
| 20-49 crops | 160 scenes | 5.2% |
| 50-99 crops | 38 scenes | 1.2% |
| 100+ crops | 8 scenes | 0.3% |

### Extreme Examples

**Scene gt_4170.jpg**: **278 text instances!**
- This is likely a very text-dense scene (e.g., newspaper, menu, poster wall)
- Contains words like: "tage", "PA", "win", "with", "home", etc.
- 1 scene → 278 training samples

**Scene gt_2852.jpg**: **187 text instances**
- Contains: "OF", "COMMUNITY", "OPMENT", "SURVIVES", etc.
- 1 scene → 187 training samples

**Scene gt_1767.jpg**: **140 text instances**
- Contains: "including", "Tory", "foodbanks", "public", etc.
- 1 scene → 140 training samples

---

## 🔍 Why This Makes Sense

### 1. **Text Recognition vs Scene Understanding**

Text recognition models don't need to understand full scenes. They need to recognize individual text instances.

```
Input to model:  [Cropped image of "COFFEE"]
Output:          "COFFEE"

NOT:
Input:           [Full storefront photo]
Output:          "COFFEE SHOP OPEN 7AM-9PM 555-1234 ..."
```

### 2. **Standard Dataset Format**

This is how ALL text recognition datasets work:
- **ICDAR datasets**: Scene images with multiple text regions
- **Total-Text**: ~1,500 scenes → ~13,700 crops (9x)
- **ArT**: ~4,400 scenes → ~32,300 crops (7x)
- **COCO-Text**: Thousands of scenes → hundreds of thousands of crops

### 3. **Training Efficiency**

Each text crop is an independent training sample:
- Model learns from diverse text instances
- More samples = better generalization
- Each crop has its own label

---

## 📈 Complete Breakdown

### ArT Dataset (Fixed - No Leakage)

| Split | Scene Images | Text Crops | Ratio |
|-------|--------------|------------|-------|
| **Train** | 3,096 | 22,726 | 7.3x |
| **Val** | 663 | 4,927 | 7.4x |
| **Test** | 664 | 4,696 | 7.1x |
| **TOTAL** | **4,423** | **32,349** | **7.3x** |

### Total-Text Dataset (Fixed - No Leakage)

| Split | Scene Images | Text Crops | Ratio |
|-------|--------------|------------|-------|
| **Train** | ~1,000 | 7,431 | ~7.4x |
| **Val** | ~250 | 1,858 | ~7.4x |
| **Test** | 300 | 2,209 | ~7.4x |
| **TOTAL** | **~1,550** | **11,498** | **~7.4x** |

### Combined (Curved Mix)

| Split | Scene Images | Text Crops |
|-------|--------------|------------|
| **Train** | ~4,100 | 30,157 |
| **Val** | ~900 | 6,785 |
| **Test** | ~1,000 | 6,905 |

---

## 🎨 Visual Example

Imagine this scene image:

```
┌─────────────────────────────────────────┐
│  🏪 COFFEE SHOP                         │
│     ☕ OPEN 7AM-9PM                     │
│     📞 555-1234                         │
│     📶 WIFI AVAILABLE                   │
│     🅿️ PARKING IN REAR                  │
│                                         │
│  [Photo of storefront with signs]       │
└─────────────────────────────────────────┘
```

**Preprocessing:**
1. Text detection finds 5 text regions
2. Each region is cropped:
   - Crop 1: "COFFEE SHOP"
   - Crop 2: "OPEN 7AM-9PM"
   - Crop 3: "555-1234"
   - Crop 4: "WIFI AVAILABLE"
   - Crop 5: "PARKING IN REAR"

**LMDB Storage:**
```
image-000000001 → [binary data of crop 1] → label: "COFFEE SHOP"
image-000000002 → [binary data of crop 2] → label: "OPEN 7AM-9PM"
image-000000003 → [binary data of crop 3] → label: "555-1234"
image-000000004 → [binary data of crop 4] → label: "WIFI AVAILABLE"
image-000000005 → [binary data of crop 5] → label: "PARKING IN REAR"
```

**Result:** 1 scene → 5 training samples

---

## ✅ Key Takeaways

1. **Scene images ≠ Training samples**
   - Scene images are the original photographs
   - Text crops are the individual training samples

2. **Average ratio: ~7-8 crops per scene**
   - Some scenes have 1 text instance
   - Some scenes have 200+ text instances
   - Average is around 7-8

3. **This is CORRECT and STANDARD**
   - All text recognition datasets work this way
   - More crops = more training data
   - Better for model generalization

4. **Your datasets are properly formatted**
   - 4,423 ArT scenes → 32,349 crops ✅
   - ~1,550 Total-Text scenes → 11,498 crops ✅
   - Ratios are normal and expected ✅

---

## 🔗 Relationship Summary

```
Official Dataset Count (Scene Images)
           ↓
    Preprocessing
    (Text Detection + Cropping)
           ↓
LMDB Dataset Count (Text Crop Samples)
           ↓
    Training Samples
    (What the model sees)
```

**Example:**
- Official ArT: ~10,000 scene images
- Our subset: 4,423 scenes
- After cropping: 32,349 text samples
- Model trains on: 32,349 individual text instances

---

*This is the standard format for text recognition datasets worldwide!*
