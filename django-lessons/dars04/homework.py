from books.models import Book
from books.models import Author
from django.db.models import Count
from django.db.models import Avg
from books.models import Category


# 1

b = Book.objects.filter(published_year__lte=2)
b

# 2

books = Book.objects.all()

for i in books:
    print(f"{i.title} | {i.price}")

# 3

b = Book.objects.order_by("-price")[:5]
b

# 4

b = Book.objects.filter(category__name="Fiction").count()
b

# 5

b = Book.objects.aggregate(avg_price=Avg("price"))
b

# 6

b = Author.objects.annotate(
    category_count=Count("book__bookcategory__category", distinct=True)
).filter(category_count__gt=3)
b

# 7

b = Category.objects.annotate(book_count=Count("bookcategory__book")).filter(
    book_count=0
)
b

# 8

books = Book.objects.values("published_year").annotate(count=Count("id"))

decades = {}

for item in books:
    year = item["published_year"]
    decade = (year // 10) * 10
    decades[decade] = decades.get(decade, 0) + item["count"]

for d, c in sorted(decades.items()):
    print(f"{d} - {c}")
