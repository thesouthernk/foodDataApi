
from fastapi import APIRouter, Response, status
from ....models.api_models import Item, ItemList
from typing import Optional, List

import pandas as pd
import os

router = APIRouter()

#Search 
@router.get("/search", response_model=ItemList)
async def search(name: str = None, category: str = None, nutrient: str = None):
    mainPath = os.path.dirname(os.path.abspath(__file__))
    data = pd.read_csv(mainPath+'/finalData.csv')
    data = data.fillna('')
    if name:
        data = data[data['description'].str.contains(name, case=False)]
    if category:
        data = data[data['foodCategory'].str.contains(category, case=False)]
    if nutrient:
        data = data[data['name'].str.contains(nutrient, case=False)]
    data = (data.groupby([data['description'],data['foodCategory']])
       .apply(lambda x: [{k:v} for k, v in zip( x['name'],x['ammount'])])
       .reset_index(name='nutrients'))
    return ItemList(items=data.to_dict(orient="records"))

@router.post("/search_by_nutrients", response_model=ItemList)
async def search_by_nutrients(nutrientsList: Optional[List[str]] = []):
    if nutrientsList != []:
        mainPath = os.path.dirname(os.path.abspath(__file__))
        data = pd.read_csv(mainPath+'/finalData.csv')
        data = data.fillna('')
        data = (data.groupby([data['name'],data['type']])
       .apply(lambda x: [{k:v} for k, v in zip( x['description'],x['ammount'])])
       .reset_index(name='food'))
        return ItemList(items=data.to_dict(orient="records"))

    else:
        mainPath = os.path.dirname(os.path.abspath(__file__))
        data = pd.read_csv(mainPath+'/finalData.csv')
        data = data.fillna('')
        data = data[data['name'].isin(nutrientsList)]
        data = (data.groupby([data['name'],data['type']])
       .apply(lambda x: [{k:v} for k, v in zip( x['description'],x['ammount'])])
       .reset_index(name='food'))
        return ItemList(items=data.to_dict(orient="records"))
    
@router.get("/nutrients", response_model=ItemList)
async def nutrients():
    mainPath = os.path.dirname(os.path.abspath(__file__))
    data = pd.read_csv(mainPath+'/finalData.csv')
    data = data.fillna('')
    nutrientsList = data['name'].unique()
    return ItemList(items=nutrientsList.tolist())


