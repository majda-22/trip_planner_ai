from crewai_tools import BaseTool
from duckduckgo_search import DDGS

class SearchInternetTool(BaseTool):
    name: str = "Search Internet"
    description: str = "Searches the internet for a given query."

    def _run(self, query: str) -> str:
        try:
            ddgs = DDGS()
            results = ddgs.text(query, max_results=5)
            
            if not results:
                return "No results found."
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. {result["title"]}\n"
                    f"   {result["body"]}\n"
                    f"   Source: {result["href"]}\n"
                )
            
            return "\n".join(formatted_results)
        
        except Exception as e:
            return f"Error during search: {str(e)}"

class SearchWeatherTool(BaseTool):
    name: str = "Search Weather"
    description: str = "Searches for weather forecasts for a specific location and date range."

    def _run(self, location: str, dates: str) -> str:
        query = f"weather forecast {location} {dates}"
        return SearchInternetTool()._run(query)

class SearchFlightsTool(BaseTool):
    name: str = "Search Flights"
    description: str = "Searches for flight information between an origin and a destination for specific dates."

    def _run(self, origin: str, destination: str, dates: str) -> str:
        query = f"flights from {origin} to {destination} on {dates} prices"
        return SearchInternetTool()._run(query)

class SearchAttractionsTool(BaseTool):
    name: str = "Search Attractions"
    description: str = "Searches for tourist attractions in a city based on interests."

    def _run(self, city: str, interests: str) -> str:
        query = f"best attractions in {city} for {interests} tourism"
        return SearchInternetTool()._run(query)