import math
import random
import time  # هذي عشان نحسب الرن تايم المطلوب في الريبورت

# ------------------------
#   قراءة ملف ال  TSP 
# -------------------------

def read_tsp_file(filename):
    cities = []
    reading = False 

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line == 'NODE_COORD_SECTION':
                reading = True 
                continue
            if line == 'EOF':
                break 

            if reading:
                parts = line.split()
                # هنا نقسم السطر لإحداثيات اكس و واي للمدينة
                x = float(parts[1])
                y = float(parts[2])
                cities.append((x, y))
    return cities


# ------------------------
#  حسابات الباث والمسافات
# ------------------------

def euclidean_distance(city1, city2):
    # نحسب الباث المستقيم بين مدينتين باستخدام قانون المسافة
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)


def total_distance(tour, cities):
    # نجمع مسافات الباث كامل ونرجع لنقطة البداية
    dist = 0
    n = len(tour)
    for i in range(n):
        city_a = cities[tour[i]]
        city_b = cities[tour[(i + 1) % n]] 
        dist += euclidean_distance(city_a, city_b)
    return dist


# -----------------------
#  ال موفمنت والتحريك
# ---------------------

def random_tour(n):
    # نسوي باث عشوائي كبداية لكل فايرفلاي
    tour = list(range(n))
    random.shuffle(tour)
    return tour


def swap_move(tour):
    # هذي حركة السواب العشوائية لازم لل اكسبلوريشن
    new_tour = tour[:] 
    i, j = random.sample(range(len(tour)), 2) 
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i] 
    return new_tour


# ---------------------------------
#   الفايرفلاي القورثم (الاساسية)
# ---------------------------------

def firefly_algorithm(cities, num_fireflies=20, num_iterations=500, alpha=0.5, seed=None):
    
    # وش السالفة هنا؟ ال (سيد) هو مثبت للراندومنس
    # حطيناه عشان لو شغلنا الكود مليون مرة تطلع نفس النتائج
    # كأنه باسوورد يخلي الراندوم يمشي بنفس الباث دايم
    if seed is not None:
        random.seed(seed)

    n = len(cities)

    # تهيئة الفايرفلايز.. كل وحدة لها باث عشوائي
    fireflies = [random_tour(n) for _ in range(num_fireflies)]
    
    # نحسب البرايتنس.. المسافة الأقصر تعني برايتنس اعلى
    brightness = [-total_distance(f, cities) for f in fireflies]

    # نتبع أحسن باث لقيناه للحظة
    best_idx = brightness.index(max(brightness))
    best_tour = fireflies[best_idx][:]
    best_distance = -brightness[best_idx]

    # اللوب الاساسي لل فايرفلاي
    for iteration in range(num_iterations):
        for i in range(num_fireflies):
            for j in range(num_fireflies):
                
                # (j) تنجذب لل (فايرفلاي) رقم (i) ال (فايرفلاي) رقم 
                # (i) أحسن من الـ (باث) حق (j) في حال كان الـ (باث) حق 
                if brightness[j] > brightness[i]:
                    
                    if random.random() < alpha:
                        # نسوي باث جديد بحركة سواب عشوائية (exploration)
                        new_tour = swap_move(fireflies[i])
                    else:
                        # نسوي باث جديد بأخذ سيجمنت من الباث الافضل (exploitation)
                        new_tour = fireflies[i][:]
                        start = random.randint(0, (n - 2))
                        end = random.randint((start + 1), (n - 1))
                        segment = fireflies[j][start:end]
                        rest = [c for c in fireflies[i] if c not in segment]
                        new_tour = (rest[:start] + segment + rest[start:])

                    # تشيك لو الباث الجديد احسن من الحالي
                    new_brightness = -total_distance(new_tour, cities)
                    if new_brightness > brightness[i]:
                        fireflies[i] = new_tour
                        brightness[i] = new_brightness

        # تحديث الجلوبال بست باث
        current_best_idx = brightness.index(max(brightness))
        if -brightness[current_best_idx] < best_distance:
            best_tour = fireflies[current_best_idx][:]
            best_distance = -brightness[current_best_idx]

    return best_tour, best_distance


# -----------------------------
#    تشغيل وحساب الرن تايم  
# ------------------------------

if __name__ == "__main__":
 
    # الداتا سيتس اللي بنشغل عليها
    instances = [
        ("data/eil51.tsp", "eil51"),
        ("data/pr264.tsp", "pr264")
    ]
 
    # نشغل على كل داتا سيت
    for filename, name in instances:
        cities = read_tsp_file(filename)
        print(f"\n{'='*50}")
        print(f"Running Firefly Algorithm on {name} ({len(cities)} cities)")
        print(f"{'='*50}")
 
        # نشغل 20 رن مختلفة بسيد مختلف لكل رن
        for seed in range(1, 21):
            start_time = time.time()
 
            best_tour, best_dist = firefly_algorithm(
                cities,
                num_fireflies=20,
                num_iterations=1000,
                alpha=0.5,
                seed=seed  # كل رن بسيد مختلف عشان النتائج تكون مستقلة
            )
 
            end_time = time.time()
            runtime = end_time - start_time
 
            # نطبع النتائج لكل رن
            print(f"Run {seed:02d} | Best Distance: {best_dist:.2f} | Runtime: {runtime:.4f}s")