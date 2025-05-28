from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import FoodItem
from .forms import FoodItemForm
from django.db.models import Sum

def food_list(request):
   
    today = timezone.localdate()
    food_items = FoodItem.objects.filter(date_consumed=today)
    total_calories = food_items.aggregate(Sum('calories'))['calories__sum'] or 0

    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.date_consumed = today 
            food_item.save()
            return redirect('food_list')
    else:
        form = FoodItemForm()

    context = {
        'food_items': food_items,
        'total_calories': total_calories,
        'form': form,
        'today': today,
    }
    return render(request, 'food_list.html', context)

def edit_food(request, pk):
   
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, instance=food_item)
        if form.is_valid():
            form.save()
            return redirect('food_list')
    else:
        form = FoodItemForm(instance=food_item)
    return render(request, 'edit_food.html', {'form': form, 'food_item': food_item})

def delete_food(request, pk):
   
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        food_item.delete()
        return redirect('food_list')
    return render(request, 'delete_food_confirm.html', {'food_item': food_item})

def reset_daily_calories(request):
   
    if request.method == 'POST':
        today = timezone.localdate()
        FoodItem.objects.filter(date_consumed=today).delete()
    return redirect('food_list')

