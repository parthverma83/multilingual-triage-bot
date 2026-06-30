#!/usr/bin/env python3
"""
Sprint 7 Integration Test Suite
Validates backend → inference service communication
"""

import asyncio
import json
import time
import sys
from datetime import datetime
import httpx


class TestSuite:
    def __init__(self, backend_url: str, inference_url: str):
        self.backend_url = backend_url.rstrip("/")
        self.inference_url = inference_url.rstrip("/")
        self.results = []
    
    async def test_inference_health(self):
        """Test inference service /health endpoint"""
        test_name = "Inference Service Health Check"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.inference_url}/health")
                response.raise_for_status()
                data = response.json()
                
                assert "status" in data, "Missing 'status' in response"
                assert data["status"] in ["healthy", "loading"], f"Invalid status: {data['status']}"
                
                print(f"✓ {test_name}")
                print(f"  Status: {data.get('status')}")
                print(f"  Model Loaded: {data.get('model_loaded')}")
                self.results.append(("PASS", test_name, None))
                return True
        except Exception as e:
            print(f"✗ {test_name}: {str(e)}")
            self.results.append(("FAIL", test_name, str(e)))
            return False
    
    async def test_backend_health(self):
        """Test backend /health endpoint"""
        test_name = "Backend Health Check"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.backend_url}/health")
                response.raise_for_status()
                data = response.json()
                
                assert "status" in data, "Missing 'status' in response"
                assert data["status"] == "healthy", f"Backend unhealthy: {data.get('status')}"
                
                print(f"✓ {test_name}")
                self.results.append(("PASS", test_name, None))
                return True
        except Exception as e:
            print(f"✗ {test_name}: {str(e)}")
            self.results.append(("FAIL", test_name, str(e)))
            return False
    
    async def test_triage_endpoint(self):
        """Test backend triage endpoint with mock data"""
        test_name = "Triage Endpoint"
        try:
            payload = {
                "message": "I have a severe headache and fever",
                "language": "en"
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                start = time.time()
                response = await client.post(
                    f"{self.backend_url}/api/v1/triage",
                    json=payload
                )
                latency = time.time() - start
                
                response.raise_for_status()
                data = response.json()
                
                assert "department" in data or "error" in data, "Invalid response format"
                
                print(f"✓ {test_name}")
                print(f"  Latency: {latency:.2f}s")
                print(f"  Response: {json.dumps(data, indent=2)}")
                self.results.append(("PASS", test_name, f"Latency: {latency:.2f}s"))
                return True
        except Exception as e:
            print(f"✗ {test_name}: {str(e)}")
            self.results.append(("FAIL", test_name, str(e)))
            return False
    
    async def test_inference_generate(self):
        """Test inference /generate endpoint directly"""
        test_name = "Inference Generate Endpoint"
        try:
            payload = {
                "prompt": "Emergency assessment: Patient with chest pain",
                "request_id": "test-123"
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                start = time.time()
                response = await client.post(
                    f"{self.inference_url}/generate",
                    json=payload
                )
                latency = time.time() - start
                
                response.raise_for_status()
                data = response.json()
                
                assert "generated_text" in data, "Missing 'generated_text' in response"
                
                print(f"✓ {test_name}")
                print(f"  Latency: {latency:.2f}s")
                print(f"  Generated: {data['generated_text'][:100]}...")
                self.results.append(("PASS", test_name, f"Latency: {latency:.2f}s"))
                return True
        except Exception as e:
            print(f"✗ {test_name}: {str(e)}")
            self.results.append(("FAIL", test_name, str(e)))
            return False
    
    async def test_error_handling(self):
        """Test error handling with invalid data"""
        test_name = "Error Handling"
        try:
            payload = {
                "message": "",  # Empty message
                "language": "invalid"
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.backend_url}/api/v1/triage",
                    json=payload
                )
                
                # Should either return 400 or handle gracefully
                assert response.status_code in [400, 422, 200], f"Unexpected status: {response.status_code}"
                
                print(f"✓ {test_name}")
                print(f"  Status Code: {response.status_code}")
                self.results.append(("PASS", test_name, None))
                return True
        except Exception as e:
            print(f"✗ {test_name}: {str(e)}")
            self.results.append(("FAIL", test_name, str(e)))
            return False
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for r in self.results if r[0] == "PASS")
        failed = sum(1 for r in self.results if r[0] == "FAIL")
        total = len(self.results)
        
        for status, name, detail in self.results:
            symbol = "✓" if status == "PASS" else "✗"
            detail_str = f" ({detail})" if detail else ""
            print(f"{symbol} {name}{detail_str}")
        
        print("="*60)
        print(f"Passed: {passed}/{total}")
        print(f"Failed: {failed}/{total}")
        print("="*60)
        
        return failed == 0


async def main():
    # Configuration
    BACKEND_URL = "http://localhost:8000"
    INFERENCE_URL = "http://localhost:8001"
    
    # Override with command line args
    if len(sys.argv) > 1:
        BACKEND_URL = sys.argv[1]
    if len(sys.argv) > 2:
        INFERENCE_URL = sys.argv[2]
    
    print(f"Starting Sprint 7 Integration Tests")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Inference URL: {INFERENCE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("="*60)
    
    suite = TestSuite(BACKEND_URL, INFERENCE_URL)
    
    # Run tests
    await suite.test_inference_health()
    await suite.test_backend_health()
    await suite.test_inference_generate()
    await suite.test_triage_endpoint()
    await suite.test_error_handling()
    
    # Print summary
    success = suite.print_summary()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
