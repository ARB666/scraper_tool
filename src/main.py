from fastapi import FastAPI
from src.scraping.router import router as scraping_router

app = FastAPI()


app.include_router(scraping_router, prefix="/scrape", tags=["scrape"])

#1. use logging                                                  - DONE
#2. clean redis atleast with fresh install                       - DONE
#3. update readme make it much better                            - DONE
#4. check ideal way to send response                             - DONE
#5. In values of request params, use "" instead of "string"      - DONE
#6. Product update logic fix                                     - DONE
#7. Check for more test cases before final build                 - 
#8. Use Exception handling                                       - DONE
#9. Save the price as integer and not string                     - 
#10.  create a new github project                                - 