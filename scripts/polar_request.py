import pymongo
import polars as pl

# Connexion Mongo
client = pymongo.MongoClient("mongodb://root:a1B2c3D4e5@localhost:27030/?replicaSet=rs0&authSource=admin")
db = client["backup"]
collection = db["listing_paris"]

# 1. Taux de réservation moyen par mois par type de logement
cursor = collection.find(
    {
        "reviews_per_month": {"$ne": None},
        "property_type": {"$ne": None}
    },
    {
        "property_type": 1,
        "reviews_per_month": 1
    }
)

df = pl.from_dicts(cursor).with_columns([
    pl.col("reviews_per_month").cast(pl.Float64, strict=False),
    pl.col("property_type").cast(pl.Utf8)
]).filter(
    pl.col("reviews_per_month").is_not_nan()
)

print("1. Taux de réservation moyen par type de logement :")
print(
    df.group_by("property_type").agg(
        pl.col("reviews_per_month").mean().alias("avg_reviews_per_month")
    ).sort("avg_reviews_per_month", descending=True)
)

# 2. Médiane du nombre d’avis pour tous les logements
cursor = collection.find(
    { "number_of_reviews": {"$ne": None} },
    { "number_of_reviews": 1 }
)

df = pl.from_dicts(cursor).with_columns(
    pl.col("number_of_reviews").cast(pl.Int64)
).filter(
    pl.col("number_of_reviews").is_not_null()
)

print("\n2. Médiane du nombre d’avis pour tous les logements :")
print(df.select(pl.col("number_of_reviews").median()))

# 3. Médiane du nombre d’avis par catégorie d’hôte
cursor = collection.find(
    {
        "number_of_reviews": {"$ne": None},
        "host_is_superhost": {"$in": ["t", "f"]}
    },
    {
        "number_of_reviews": 1,
        "host_is_superhost": 1
    }
)

df = pl.from_dicts(cursor).with_columns([
    pl.col("number_of_reviews").cast(pl.Int64),
    pl.col("host_is_superhost").cast(pl.Utf8)
]).filter(
    pl.col("number_of_reviews").is_not_null()
)

print("\n3. Médiane des avis par catégorie d’hôte :")
print(
    df.group_by("host_is_superhost").agg(
        pl.col("number_of_reviews").median().alias("median_reviews")
    )
)

# 4. Densité de logements par quartier de Paris
cursor = collection.find(
    { "neighbourhood_cleansed": {"$ne": None} },
    { "neighbourhood_cleansed": 1 }
)

df = pl.from_dicts(cursor).with_columns(
    pl.col("neighbourhood_cleansed").cast(pl.Utf8)
)

print("\n4. Densité de logements par quartier :")
print(
    df.group_by("neighbourhood_cleansed").agg(
        pl.len().alias("count_listings")
    ).sort("count_listings", descending=True)
)

# 5. Quartiers avec le plus fort taux de réservation par mois
cursor = collection.find(
    {
        "reviews_per_month": {"$ne": None},
        "neighbourhood_cleansed": {"$ne": None}
    },
    {
        "reviews_per_month": 1,
        "neighbourhood_cleansed": 1
    }
)

df = pl.from_dicts(cursor).with_columns([
    pl.col("reviews_per_month").cast(pl.Float64, strict=False),
    pl.col("neighbourhood_cleansed").cast(pl.Utf8)
]).filter(
    pl.col("reviews_per_month").is_not_nan()
)


print("\n5. Quartiers avec le plus fort taux de réservation :")
print(
    df.group_by("neighbourhood_cleansed").agg(
        pl.col("reviews_per_month").mean().alias("avg_reviews_per_month")
    ).sort("avg_reviews_per_month", descending=True)
)
