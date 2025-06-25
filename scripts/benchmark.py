"""Benchmark script for DocuRAG API."""

import asyncio
import time
from statistics import mean, median
from typing import List, Dict, Any

import aiohttp
import argparse


class BenchmarkRunner:
    """Run benchmark tests against DocuRAG API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize benchmark runner.
        
        Args:
            base_url: Base URL of the API
        """
        self.base_url = base_url
        self.query_url = f"{base_url}/query"
        self.health_url = f"{base_url}/healthz"
    
    async def check_health(self) -> bool:
        """Check if the API is healthy.
        
        Returns:
            True if API is healthy, False otherwise
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.health_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("status") == "healthy"
            return False
        except Exception:
            return False
    
    async def single_query(
        self, 
        session: aiohttp.ClientSession, 
        question: str
    ) -> Dict[str, Any]:
        """Execute a single query and measure performance.
        
        Args:
            session: HTTP session
            question: Question to ask
            
        Returns:
            Dictionary with timing and response information
        """
        start_time = time.time()
        
        try:
            async with session.post(
                self.query_url,
                json={"question": question}
            ) as response:
                end_time = time.time()
                
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "response_time": end_time - start_time,
                        "status_code": response.status,
                        "answer_length": len(data.get("answer", "")),
                        "num_sources": len(data.get("sources", []))
                    }
                else:
                    return {
                        "success": False,
                        "response_time": end_time - start_time,
                        "status_code": response.status,
                        "error": await response.text()
                    }
        except Exception as e:
            end_time = time.time()
            return {
                "success": False,
                "response_time": end_time - start_time,
                "status_code": 0,
                "error": str(e)
            }
    
    async def run_benchmark(
        self, 
        num_requests: int = 1000, 
        concurrency: int = 10,
        questions: List[str] = None
    ) -> Dict[str, Any]:
        """Run benchmark with multiple concurrent requests.
        
        Args:
            num_requests: Total number of requests to make
            concurrency: Number of concurrent requests
            questions: List of questions to cycle through
            
        Returns:
            Benchmark results
        """
        if questions is None:
            questions = [
                "What is this document about?",
                "Can you summarize the main points?",
                "What are the key findings?",
                "Who are the authors?",
                "What is the conclusion?"
            ]
        
        print(f"Running benchmark: {num_requests} requests with {concurrency} concurrent connections")
        print(f"Target URL: {self.query_url}")
        
        # Check health first
        if not await self.check_health():
            raise RuntimeError("API is not healthy")
        
        results = []
        semaphore = asyncio.Semaphore(concurrency)
        
        async def bounded_query(session: aiohttp.ClientSession, question: str):
            async with semaphore:
                return await self.single_query(session, question)
        
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(num_requests):
                question = questions[i % len(questions)]
                task = bounded_query(session, question)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        return self._analyze_results(results, total_time)
    
    def _analyze_results(self, results: List[Dict[str, Any]], total_time: float) -> Dict[str, Any]:
        """Analyze benchmark results.
        
        Args:
            results: List of individual request results
            total_time: Total benchmark time
            
        Returns:
            Analysis summary
        """
        successful_results = [r for r in results if r["success"]]
        failed_results = [r for r in results if not r["success"]]
        
        if successful_results:
            response_times = [r["response_time"] for r in successful_results]
            answer_lengths = [r["answer_length"] for r in successful_results]
            num_sources = [r["num_sources"] for r in successful_results]
        else:
            response_times = answer_lengths = num_sources = []
        
        return {
            "total_requests": len(results),
            "successful_requests": len(successful_results),
            "failed_requests": len(failed_results),
            "success_rate": len(successful_results) / len(results) * 100,
            "total_time": total_time,
            "requests_per_second": len(results) / total_time,
            "response_times": {
                "mean": mean(response_times) if response_times else 0,
                "median": median(response_times) if response_times else 0,
                "min": min(response_times) if response_times else 0,
                "max": max(response_times) if response_times else 0
            },
            "answer_stats": {
                "mean_length": mean(answer_lengths) if answer_lengths else 0,
                "mean_sources": mean(num_sources) if num_sources else 0
            },
            "errors": [r.get("error") for r in failed_results]
        }
    
    def format_results_markdown(self, results: Dict[str, Any]) -> str:
        """Format results as a Markdown table.
        
        Args:
            results: Benchmark results
            
        Returns:
            Formatted Markdown string
        """
        md = "# DocuRAG Benchmark Results\n\n"
        
        md += "## Summary\n\n"
        md += "| Metric | Value |\n"
        md += "|--------|-------|\n"
        md += f"| Total Requests | {results['total_requests']} |\n"
        md += f"| Successful Requests | {results['successful_requests']} |\n"
        md += f"| Failed Requests | {results['failed_requests']} |\n"
        md += f"| Success Rate | {results['success_rate']:.2f}% |\n"
        md += f"| Total Time | {results['total_time']:.2f}s |\n"
        md += f"| Requests/Second | {results['requests_per_second']:.2f} |\n\n"
        
        md += "## Response Time Statistics\n\n"
        md += "| Statistic | Value (seconds) |\n"
        md += "|-----------|----------------|\n"
        md += f"| Mean | {results['response_times']['mean']:.3f} |\n"
        md += f"| Median | {results['response_times']['median']:.3f} |\n"
        md += f"| Min | {results['response_times']['min']:.3f} |\n"
        md += f"| Max | {results['response_times']['max']:.3f} |\n\n"
        
        md += "## Answer Statistics\n\n"
        md += "| Metric | Value |\n"
        md += "|--------|-------|\n"
        md += f"| Mean Answer Length | {results['answer_stats']['mean_length']:.0f} chars |\n"
        md += f"| Mean Sources per Answer | {results['answer_stats']['mean_sources']:.1f} |\n\n"
        
        if results['errors']:
            md += "## Errors\n\n"
            for i, error in enumerate(results['errors'][:5], 1):  # Show first 5 errors
                md += f"{i}. {error}\n"
            if len(results['errors']) > 5:
                md += f"... and {len(results['errors']) - 5} more errors\n"
        
        return md


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Benchmark DocuRAG API")
    parser.add_argument("--url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--requests", type=int, default=1000, help="Number of requests")
    parser.add_argument("--concurrency", type=int, default=10, help="Concurrent connections")
    parser.add_argument("--output", help="Output file for results")
    
    args = parser.parse_args()
    
    runner = BenchmarkRunner(args.url)
    
    try:
        results = await runner.run_benchmark(
            num_requests=args.requests,
            concurrency=args.concurrency
        )
        
        markdown_output = runner.format_results_markdown(results)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(markdown_output)
            print(f"Results saved to {args.output}")
        else:
            print(markdown_output)
    
    except Exception as e:
        print(f"Benchmark failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))