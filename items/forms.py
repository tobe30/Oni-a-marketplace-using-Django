from django import forms
from core.models import Product, ProductImages, Category, Brand
from taggit.forms import TagField  # Import the tag field


class NewItemForm(forms.ModelForm):
    
    CONDITION_CHOICES = (
    ("new", "new"),
    ("used", "used"),
    ("old", "old"),
    ("refurbished", "refurbished"),
    ("renovated", "renovated"),
    
    

)
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Type your product title here", 
        "class":"form-control"
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Describe your message", 
        "class":"form-control"
    }))
    

    link = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Type your Youtube link", 
        "class":"form-control"
    }), required=False)
    price = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': "Enter your pricing amount", 
        "class":"form-control"
    }))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),  # Fetch all categories from the database
        widget=forms.Select(attrs={
            'class': 'form-control custom-select',
            'required': 'required',
            'id': 'category'
        }),
        empty_label="Select category",  # This will be the first option in the dropdown
    )
    condition = forms.ChoiceField(
        choices=CONDITION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control custom-select',
            'required': 'required',
        }),
        initial='',  # This makes sure the first option is not pre-selected
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),  # Fetch all categories from the database
        widget=forms.Select(attrs={
            'class': 'form-control custom-select',
            'required': 'required',
        }),
        empty_label="Select Brand"  # This will be the first option in the dropdown
    )
    
    
    year = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': "Enter year", 
        "class":"form-control"
    }), required=False)
    size = forms.CharField(widget=forms.TextInput(attrs={
        "id": "size", 
        'placeholder': "Enter the sizes of item e.g., phone, car etc..", 
        "class":"form-control"
    }), required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Enter your location", 
        "class":"form-control"
    }), required=False)
    warranty = forms.CharField(widget=forms.TextInput(attrs={
        "id": "warranty", 
        'placeholder': "Enter Warranty details", 
        "class":"form-control"
    }), required=False)
    color = forms.CharField(widget=forms.TextInput(attrs={
        "id": "color", 
        'placeholder': "Enter color", 
        "class":"form-control"
    }), required=False)
    features = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Describe your Features", 
        "class":"form-control"
    }), required=False)
    mileage = forms.IntegerField(widget=forms.NumberInput(attrs={
        "id": "mileage", 
        'placeholder': "Enter mileage", 
        "class":"form-control"
    }), required=False)
    transmission = forms.CharField(widget=forms.TextInput(attrs={
        "id": "transmission", 
        'placeholder': "Enter transmission type", 
        "class":"form-control"
    }), required=False)
    fuel_type = forms.CharField(widget=forms.TextInput(attrs={
        "id": "fuel_type", 
        'placeholder': "Enter fuel type", 
        "class":"form-control"
    }), required=False)
    engine_size = forms.CharField(widget=forms.TextInput(attrs={
        "id": "engine_size", 
        'placeholder': "Enter engine size", 
        "class":"form-control"
    }), required=False)
    number_of_doors = forms.IntegerField(widget=forms.NumberInput(attrs={
        "id": "number_of_doors", 
        'placeholder': "Enter number of doors", 
        "class":"form-control"
    }), required=False)
    number_of_seats = forms.IntegerField(widget=forms.NumberInput(attrs={
        "id": "number_of_seats", 
        'placeholder': "Enter number of seats", 
        "class":"form-control"
    }), required=False)
    property_type = forms.CharField(widget=forms.TextInput(attrs={
        "id": "property_type", 
        'placeholder': "Enter property type", 
        "class":"form-control"
    }), required=False)
    bedrooms = forms.IntegerField(widget=forms.NumberInput(attrs={
        "id": "bedrooms", 
        'placeholder': "Enter number of bedrooms", 
        "class":"form-control"
    }), required=False)
    bathrooms = forms.IntegerField(widget=forms.NumberInput(attrs={
        "id": "bathrooms", 
        'placeholder': "Enter number of bathrooms", 
        "class":"form-control"
    }), required=False)
    square_feet = forms.IntegerField(widget=forms.NumberInput(attrs={
        "id": "square_feet", 
        'placeholder': "Enter square feet", 
        "class":"form-control"
    }), required=False)
    lot_size = forms.IntegerField(widget=forms.NumberInput(attrs={
        "id": "lot_size", 
        'placeholder': "Enter lot size", 
        "class":"form-control"
    }), required=False)
    year_built = forms.CharField(widget=forms.NumberInput(attrs={
        "id": "year_built", 
        'placeholder': "Enter year built", 
        "class":"form-control"
    }), required=False)
    screen_size = forms.CharField(widget=forms.TextInput(attrs={
        "id": "screen_size", 
        'placeholder': "Enter screen size", 
        "class":"form-control"
    }), required=False)
    battery_life = forms.CharField(widget=forms.TextInput(attrs={
        "id": "battery_life", 
        'placeholder': "Enter battery life", 
        "class":"form-control"
    }), required=False)
    storage_capacity = forms.CharField(widget=forms.TextInput(attrs={
        "id": "storage_capacity", 
        'placeholder': "Enter storage capacity", 
        "class":"form-control"
    }), required=False)
    ram = forms.CharField(widget=forms.TextInput(attrs={
        "id": "ram", 
        'placeholder': "Enter RAM size", 
        "class":"form-control"
    }), required=False)
    processor = forms.CharField(widget=forms.TextInput(attrs={
        "id": "processor", 
        'placeholder': "Enter processor type", 
        "class":"form-control"
    }), required=False)
    camera_quality = forms.CharField(widget=forms.TextInput(attrs={
        "id": "camera_quality", 
        'placeholder': "Enter camera quality", 
        "class":"form-control"
    }), required=False)
    material = forms.CharField(widget=forms.TextInput(attrs={
        "id": "material", 
        'placeholder': "Enter material type", 
        "class":"form-control"
    }), required=False)
    dimensions = forms.CharField(widget=forms.TextInput(attrs={
        "id": "dimensions", 
        'placeholder': "Enter dimensions", 
        "class":"form-control"
    }), required=False)
    weight = forms.CharField(widget=forms.TextInput(attrs={
        "id": "weight", 
        'placeholder': "Enter weight", 
        "class":"form-control"
    }), required=False)
    clothing_size = forms.CharField(widget=forms.TextInput(attrs={
        "id": "clothing_size", 
        'placeholder': "Enter clothing size", 
        "class":"form-control"
    }), required=False)
    fabric_type = forms.CharField(widget=forms.TextInput(attrs={
        "id": "fabric_type", 
        'placeholder': "Enter fabric type", 
        "class":"form-control"
    }), required=False)
    age_group = forms.CharField(widget=forms.TextInput(attrs={
        "id": "age_group", 
        'placeholder': "Enter age group", 
        "class":"form-control"
    }), required=False)
    safety_standards = forms.CharField(widget=forms.TextInput(attrs={
        "id": "safety_standards", 
        'placeholder': "Enter safety standards", 
        "class":"form-control"
    }), required=False)
    tags = TagField(widget=forms.TextInput(attrs={
        'placeholder': "Add tags (comma-separated)", 
        "class": "form-control"
    }), required=False)
    
    # Image Upload Field
    
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',
        'id': 'imageInput1',
        'onchange': "displayImage('imageInput1', 'image1')"
    }))
    
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'category', 'condition', 'link', 'price', 'year', 'size', 'location',
            'warranty', 'color', 'features', 'mileage', 'transmission', 'fuel_type',
            'engine_size', 'number_of_doors', 'number_of_seats', 'property_type', 
            'bedrooms', 'bathrooms', 'square_feet', 'lot_size', 'screen_size', 
            'battery_life', 'storage_capacity', 'ram', 'processor', 'camera_quality', 
            'material', 'dimensions', 'weight', 'clothing_size', 'fabric_type', 
            'age_group', 'safety_standards', 'tags',  'image', 'brand'
        ]
        
def save(self, commit=True):
        product = super().save(commit=False)

        if commit:
            product.save()
            # Save tags
            self.save_m2m()  # Required for saving many-to-many relationships (tags)

        return product
        
class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['images']



