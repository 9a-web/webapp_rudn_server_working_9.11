#!/usr/bin/env python3
"""
Test Admin Endpoints Only
"""

import requests
import json
import sys
import time

class AdminEndpointTester:
    def __init__(self):
        self.base_url = "http://localhost:8001/api"
        self.session = requests.Session()
        self.session.timeout = 30
        self.test_results = []

    def log_test(self, test_name: str, success: bool, message: str, details=None):
        """Log test result"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'details': details
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if details and success:
            print(f"   📊 Details: {json.dumps(details, indent=2, ensure_ascii=False)}")

    def test_admin_stats_endpoint(self) -> bool:
        """Test GET /api/admin/stats endpoint with different parameters"""
        try:
            print("🔍 Testing GET /api/admin/stats...")
            
            # Test 1: Without parameters (all time)
            response = self.session.get(f"{self.base_url}/admin/stats")
            
            if response.status_code != 200:
                self.log_test("GET /api/admin/stats (all time)", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            stats_all = response.json()
            
            # Validate response structure
            required_fields = ['total_users', 'active_users_today', 'active_users_week', 'active_users_month',
                             'new_users_today', 'new_users_week', 'new_users_month', 'total_tasks',
                             'total_completed_tasks', 'total_achievements_earned', 'total_rooms', 'total_schedule_views']
            
            for field in required_fields:
                if field not in stats_all:
                    self.log_test("GET /api/admin/stats (all time)", False, 
                                f"Missing required field: {field}")
                    return False
                
                if not isinstance(stats_all[field], int):
                    self.log_test("GET /api/admin/stats (all time)", False, 
                                f"Field {field} should be integer, got {type(stats_all[field])}")
                    return False
            
            # Test 2: With days=7 parameter
            response_7 = self.session.get(f"{self.base_url}/admin/stats?days=7")
            
            if response_7.status_code != 200:
                self.log_test("GET /api/admin/stats (days=7)", False, 
                            f"HTTP {response_7.status_code}: {response_7.text}")
                return False
            
            stats_7 = response_7.json()
            
            # Validate same structure
            for field in required_fields:
                if field not in stats_7:
                    self.log_test("GET /api/admin/stats (days=7)", False, 
                                f"Missing required field: {field}")
                    return False
            
            # Test 3: With days=30 parameter
            response_30 = self.session.get(f"{self.base_url}/admin/stats?days=30")
            
            if response_30.status_code != 200:
                self.log_test("GET /api/admin/stats (days=30)", False, 
                            f"HTTP {response_30.status_code}: {response_30.text}")
                return False
            
            stats_30 = response_30.json()
            
            # Validate same structure
            for field in required_fields:
                if field not in stats_30:
                    self.log_test("GET /api/admin/stats (days=30)", False, 
                                f"Missing required field: {field}")
                    return False
            
            self.log_test("GET /api/admin/stats", True, 
                        "Successfully tested admin stats endpoint with all parameter variations",
                        {
                            "all_time_total_users": stats_all['total_users'],
                            "all_time_total_tasks": stats_all['total_tasks'],
                            "all_time_schedule_views": stats_all['total_schedule_views'],
                            "7_days_total_tasks": stats_7['total_tasks'],
                            "30_days_total_tasks": stats_30['total_tasks'],
                            "parameters_tested": ["no parameters (all time)", "days=7", "days=30"]
                        })
            return True
            
        except Exception as e:
            self.log_test("GET /api/admin/stats", False, f"Exception: {str(e)}")
            return False

    def test_admin_users_activity_endpoint(self) -> bool:
        """Test GET /api/admin/users-activity endpoint"""
        try:
            print("🔍 Testing GET /api/admin/users-activity...")
            
            response = self.session.get(f"{self.base_url}/admin/users-activity?days=7")
            
            if response.status_code != 200:
                self.log_test("GET /api/admin/users-activity", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            activity_data = response.json()
            
            # Validate response structure
            if not isinstance(activity_data, list):
                self.log_test("GET /api/admin/users-activity", False, 
                            "Response should be a list")
                return False
            
            # Validate each activity point (if any data exists)
            for point in activity_data:
                if not isinstance(point, dict):
                    self.log_test("GET /api/admin/users-activity", False, 
                                "Activity point should be a dictionary")
                    return False
                
                required_fields = ['date', 'count']
                for field in required_fields:
                    if field not in point:
                        self.log_test("GET /api/admin/users-activity", False, 
                                    f"Activity point missing required field: {field}")
                        return False
                
                # Validate date format (YYYY-MM-DD)
                import re
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', point['date']):
                    self.log_test("GET /api/admin/users-activity", False, 
                                f"Invalid date format: {point['date']}, expected YYYY-MM-DD")
                    return False
                
                # Validate count is integer
                if not isinstance(point['count'], int):
                    self.log_test("GET /api/admin/users-activity", False, 
                                f"Count should be integer, got {type(point['count'])}")
                    return False
            
            self.log_test("GET /api/admin/users-activity", True, 
                        "Successfully retrieved user registration activity by date",
                        {
                            "data_points": len(activity_data),
                            "sample_point": activity_data[0] if activity_data else "No data",
                            "date_format": "YYYY-MM-DD",
                            "parameter_tested": "days=7"
                        })
            return True
            
        except Exception as e:
            self.log_test("GET /api/admin/users-activity", False, f"Exception: {str(e)}")
            return False

    def test_admin_hourly_activity_endpoint(self) -> bool:
        """Test GET /api/admin/hourly-activity endpoint"""
        try:
            print("🔍 Testing GET /api/admin/hourly-activity...")
            
            response = self.session.get(f"{self.base_url}/admin/hourly-activity?days=7")
            
            if response.status_code != 200:
                self.log_test("GET /api/admin/hourly-activity", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            hourly_data = response.json()
            
            # Validate response structure
            if not isinstance(hourly_data, list):
                self.log_test("GET /api/admin/hourly-activity", False, 
                            "Response should be a list")
                return False
            
            # Should have exactly 24 hours (0-23)
            if len(hourly_data) != 24:
                self.log_test("GET /api/admin/hourly-activity", False, 
                            f"Expected 24 hours, got {len(hourly_data)}")
                return False
            
            # Validate each hour point
            hours_found = set()
            for point in hourly_data:
                if not isinstance(point, dict):
                    self.log_test("GET /api/admin/hourly-activity", False, 
                                "Hour point should be a dictionary")
                    return False
                
                required_fields = ['hour', 'count']
                for field in required_fields:
                    if field not in point:
                        self.log_test("GET /api/admin/hourly-activity", False, 
                                    f"Hour point missing required field: {field}")
                        return False
                
                # Validate hour is 0-23
                if not isinstance(point['hour'], int) or point['hour'] < 0 or point['hour'] > 23:
                    self.log_test("GET /api/admin/hourly-activity", False, 
                                f"Invalid hour: {point['hour']}, expected 0-23")
                    return False
                
                hours_found.add(point['hour'])
                
                # Validate count is integer
                if not isinstance(point['count'], int):
                    self.log_test("GET /api/admin/hourly-activity", False, 
                                f"Count should be integer, got {type(point['count'])}")
                    return False
            
            # Verify all hours 0-23 are present
            expected_hours = set(range(24))
            if hours_found != expected_hours:
                missing_hours = expected_hours - hours_found
                self.log_test("GET /api/admin/hourly-activity", False, 
                            f"Missing hours: {missing_hours}")
                return False
            
            self.log_test("GET /api/admin/hourly-activity", True, 
                        "Successfully retrieved hourly activity data",
                        {
                            "hours_count": len(hourly_data),
                            "hours_range": "0-23",
                            "sample_hour": hourly_data[0] if hourly_data else None,
                            "parameter_tested": "days=7"
                        })
            return True
            
        except Exception as e:
            self.log_test("GET /api/admin/hourly-activity", False, f"Exception: {str(e)}")
            return False

    def test_admin_weekly_activity_endpoint(self) -> bool:
        """Test GET /api/admin/weekly-activity endpoint"""
        try:
            print("🔍 Testing GET /api/admin/weekly-activity...")
            
            response = self.session.get(f"{self.base_url}/admin/weekly-activity?days=30")
            
            if response.status_code != 200:
                self.log_test("GET /api/admin/weekly-activity", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            weekly_data = response.json()
            
            # Validate response structure
            if not isinstance(weekly_data, list):
                self.log_test("GET /api/admin/weekly-activity", False, 
                            "Response should be a list")
                return False
            
            # Should have exactly 7 days
            if len(weekly_data) != 7:
                self.log_test("GET /api/admin/weekly-activity", False, 
                            f"Expected 7 days, got {len(weekly_data)}")
                return False
            
            # Expected Russian day names
            expected_days = ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"]
            days_found = []
            
            # Validate each day point
            for point in weekly_data:
                if not isinstance(point, dict):
                    self.log_test("GET /api/admin/weekly-activity", False, 
                                "Day point should be a dictionary")
                    return False
                
                required_fields = ['day', 'count']
                for field in required_fields:
                    if field not in point:
                        self.log_test("GET /api/admin/weekly-activity", False, 
                                    f"Day point missing required field: {field}")
                        return False
                
                # Validate day name is in Russian
                if point['day'] not in expected_days:
                    self.log_test("GET /api/admin/weekly-activity", False, 
                                f"Invalid day name: {point['day']}, expected one of {expected_days}")
                    return False
                
                days_found.append(point['day'])
                
                # Validate count is integer
                if not isinstance(point['count'], int):
                    self.log_test("GET /api/admin/weekly-activity", False, 
                                f"Count should be integer, got {type(point['count'])}")
                    return False
            
            # Verify all days are present in correct order
            if days_found != expected_days:
                self.log_test("GET /api/admin/weekly-activity", False, 
                            f"Days order mismatch. Expected: {expected_days}, Got: {days_found}")
                return False
            
            self.log_test("GET /api/admin/weekly-activity", True, 
                        "Successfully retrieved weekly activity data",
                        {
                            "days_count": len(weekly_data),
                            "days_order": days_found,
                            "sample_day": weekly_data[0] if weekly_data else None,
                            "parameter_tested": "days=30"
                        })
            return True
            
        except Exception as e:
            self.log_test("GET /api/admin/weekly-activity", False, f"Exception: {str(e)}")
            return False

    def test_admin_feature_usage_endpoint(self) -> bool:
        """Test GET /api/admin/feature-usage endpoint"""
        try:
            print("🔍 Testing GET /api/admin/feature-usage...")
            
            response = self.session.get(f"{self.base_url}/admin/feature-usage")
            
            if response.status_code != 200:
                self.log_test("GET /api/admin/feature-usage", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            feature_data = response.json()
            
            # Validate response structure
            if not isinstance(feature_data, dict):
                self.log_test("GET /api/admin/feature-usage", False, 
                            "Response should be a dictionary")
                return False
            
            # Check required fields
            required_fields = ['schedule_views', 'analytics_views', 'calendar_opens', 
                             'notifications_configured', 'schedule_shares', 'tasks_created', 'achievements_earned']
            
            for field in required_fields:
                if field not in feature_data:
                    self.log_test("GET /api/admin/feature-usage", False, 
                                f"Missing required field: {field}")
                    return False
                
                # Validate all fields are integers
                if not isinstance(feature_data[field], int):
                    self.log_test("GET /api/admin/feature-usage", False, 
                                f"Field {field} should be integer, got {type(feature_data[field])}")
                    return False
                
                # Validate non-negative values
                if feature_data[field] < 0:
                    self.log_test("GET /api/admin/feature-usage", False, 
                                f"Field {field} should be non-negative, got {feature_data[field]}")
                    return False
            
            self.log_test("GET /api/admin/feature-usage", True, 
                        "Successfully retrieved feature usage statistics",
                        {
                            "schedule_views": feature_data['schedule_views'],
                            "analytics_views": feature_data['analytics_views'],
                            "calendar_opens": feature_data['calendar_opens'],
                            "notifications_configured": feature_data['notifications_configured'],
                            "schedule_shares": feature_data['schedule_shares'],
                            "tasks_created": feature_data['tasks_created'],
                            "achievements_earned": feature_data['achievements_earned']
                        })
            return True
            
        except Exception as e:
            self.log_test("GET /api/admin/feature-usage", False, f"Exception: {str(e)}")
            return False

    def test_admin_top_users_endpoint(self) -> bool:
        """Test GET /api/admin/top-users endpoint"""
        try:
            print("🔍 Testing GET /api/admin/top-users...")
            
            response = self.session.get(f"{self.base_url}/admin/top-users?metric=points&limit=10")
            
            if response.status_code != 200:
                self.log_test("GET /api/admin/top-users", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            top_users = response.json()
            
            # Validate response structure
            if not isinstance(top_users, list):
                self.log_test("GET /api/admin/top-users", False, 
                            "Response should be a list")
                return False
            
            # Should not exceed limit of 10
            if len(top_users) > 10:
                self.log_test("GET /api/admin/top-users", False, 
                            f"Expected max 10 users, got {len(top_users)}")
                return False
            
            # Validate each user entry (if any users exist)
            for user in top_users:
                if not isinstance(user, dict):
                    self.log_test("GET /api/admin/top-users", False, 
                                "User entry should be a dictionary")
                    return False
                
                required_fields = ['telegram_id', 'username', 'first_name', 'value', 'group_name']
                for field in required_fields:
                    if field not in user:
                        self.log_test("GET /api/admin/top-users", False, 
                                    f"User entry missing required field: {field}")
                        return False
                
                # Validate telegram_id is integer
                if not isinstance(user['telegram_id'], int):
                    self.log_test("GET /api/admin/top-users", False, 
                                f"telegram_id should be integer, got {type(user['telegram_id'])}")
                    return False
                
                # Validate value is integer (points)
                if not isinstance(user['value'], int):
                    self.log_test("GET /api/admin/top-users", False, 
                                f"value should be integer, got {type(user['value'])}")
                    return False
            
            # Verify users are sorted by value (descending) if there are users
            if len(top_users) > 1:
                for i in range(len(top_users) - 1):
                    if top_users[i]['value'] < top_users[i + 1]['value']:
                        self.log_test("GET /api/admin/top-users", False, 
                                    "Users should be sorted by value in descending order")
                        return False
            
            self.log_test("GET /api/admin/top-users", True, 
                        "Successfully retrieved top users by points",
                        {
                            "users_count": len(top_users),
                            "metric": "points",
                            "limit": 10,
                            "top_user": top_users[0] if top_users else "No users found",
                            "sorted_descending": True
                        })
            return True
            
        except Exception as e:
            self.log_test("GET /api/admin/top-users", False, f"Exception: {str(e)}")
            return False

    def test_admin_faculty_stats_endpoint(self) -> bool:
        """Test GET /api/admin/faculty-stats endpoint"""
        try:
            print("🔍 Testing GET /api/admin/faculty-stats...")
            
            response = self.session.get(f"{self.base_url}/admin/faculty-stats")
            
            if response.status_code != 200:
                self.log_test("GET /api/admin/faculty-stats", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            faculty_stats = response.json()
            
            # Validate response structure
            if not isinstance(faculty_stats, list):
                self.log_test("GET /api/admin/faculty-stats", False, 
                            "Response should be a list")
                return False
            
            # Validate each faculty entry (if any faculties exist)
            for faculty in faculty_stats:
                if not isinstance(faculty, dict):
                    self.log_test("GET /api/admin/faculty-stats", False, 
                                "Faculty entry should be a dictionary")
                    return False
                
                required_fields = ['faculty_name', 'faculty_id', 'users_count']
                for field in required_fields:
                    if field not in faculty:
                        self.log_test("GET /api/admin/faculty-stats", False, 
                                    f"Faculty entry missing required field: {field}")
                        return False
                
                # Validate faculty_name is string
                if not isinstance(faculty['faculty_name'], str):
                    self.log_test("GET /api/admin/faculty-stats", False, 
                                f"faculty_name should be string, got {type(faculty['faculty_name'])}")
                    return False
                
                # Validate users_count is integer
                if not isinstance(faculty['users_count'], int):
                    self.log_test("GET /api/admin/faculty-stats", False, 
                                f"users_count should be integer, got {type(faculty['users_count'])}")
                    return False
                
                # Validate users_count is positive
                if faculty['users_count'] <= 0:
                    self.log_test("GET /api/admin/faculty-stats", False, 
                                f"users_count should be positive, got {faculty['users_count']}")
                    return False
            
            # Verify faculties are sorted by count (descending) if there are faculties
            if len(faculty_stats) > 1:
                for i in range(len(faculty_stats) - 1):
                    if faculty_stats[i]['users_count'] < faculty_stats[i + 1]['users_count']:
                        self.log_test("GET /api/admin/faculty-stats", False, 
                                    "Faculties should be sorted by users_count in descending order")
                        return False
            
            self.log_test("GET /api/admin/faculty-stats", True, 
                        "Successfully retrieved faculty distribution statistics",
                        {
                            "faculties_count": len(faculty_stats),
                            "top_faculty": faculty_stats[0] if faculty_stats else "No faculties found",
                            "sorted_by_users_count": True
                        })
            return True
            
        except Exception as e:
            self.log_test("GET /api/admin/faculty-stats", False, f"Exception: {str(e)}")
            return False

    def test_admin_course_stats_endpoint(self) -> bool:
        """Test GET /api/admin/course-stats endpoint"""
        try:
            print("🔍 Testing GET /api/admin/course-stats...")
            
            response = self.session.get(f"{self.base_url}/admin/course-stats")
            
            if response.status_code != 200:
                self.log_test("GET /api/admin/course-stats", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            course_stats = response.json()
            
            # Validate response structure
            if not isinstance(course_stats, list):
                self.log_test("GET /api/admin/course-stats", False, 
                            "Response should be a list")
                return False
            
            # Validate each course entry (if any courses exist)
            for course in course_stats:
                if not isinstance(course, dict):
                    self.log_test("GET /api/admin/course-stats", False, 
                                "Course entry should be a dictionary")
                    return False
                
                required_fields = ['course', 'users_count']
                for field in required_fields:
                    if field not in course:
                        self.log_test("GET /api/admin/course-stats", False, 
                                    f"Course entry missing required field: {field}")
                        return False
                
                # Validate course is string
                if not isinstance(course['course'], str):
                    self.log_test("GET /api/admin/course-stats", False, 
                                f"course should be string, got {type(course['course'])}")
                    return False
                
                # Validate users_count is integer
                if not isinstance(course['users_count'], int):
                    self.log_test("GET /api/admin/course-stats", False, 
                                f"users_count should be integer, got {type(course['users_count'])}")
                    return False
                
                # Validate users_count is positive
                if course['users_count'] <= 0:
                    self.log_test("GET /api/admin/course-stats", False, 
                                f"users_count should be positive, got {course['users_count']}")
                    return False
            
            # Verify courses are sorted by course number (ascending) if there are courses
            if len(course_stats) > 1:
                course_numbers = []
                for course in course_stats:
                    try:
                        course_numbers.append(int(course['course']))
                    except ValueError:
                        # If course is not a number, skip sorting check
                        pass
                
                if len(course_numbers) > 1:
                    for i in range(len(course_numbers) - 1):
                        if course_numbers[i] > course_numbers[i + 1]:
                            self.log_test("GET /api/admin/course-stats", False, 
                                        "Courses should be sorted by course number in ascending order")
                            return False
            
            self.log_test("GET /api/admin/course-stats", True, 
                        "Successfully retrieved course distribution statistics",
                        {
                            "courses_count": len(course_stats),
                            "sample_course": course_stats[0] if course_stats else "No courses found",
                            "sorted_by_course_number": True
                        })
            return True
            
        except Exception as e:
            self.log_test("GET /api/admin/course-stats", False, f"Exception: {str(e)}")
            return False

    def run_admin_tests(self) -> bool:
        """Run all admin endpoint tests"""
        print("🚀 Starting Admin Endpoints Tests...")
        print(f"📡 Backend URL: {self.base_url}")
        print("=" * 80)
        
        # Admin tests
        admin_tests = [
            self.test_admin_stats_endpoint,
            self.test_admin_users_activity_endpoint,
            self.test_admin_hourly_activity_endpoint,
            self.test_admin_weekly_activity_endpoint,
            self.test_admin_feature_usage_endpoint,
            self.test_admin_top_users_endpoint,
            self.test_admin_faculty_stats_endpoint,
            self.test_admin_course_stats_endpoint
        ]
        
        passed = 0
        failed = 0
        
        for test in admin_tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ EXCEPTION in {test.__name__}: {str(e)}")
                failed += 1
            
            # Small delay between tests
            time.sleep(0.5)
        
        # Print summary
        print("=" * 80)
        print("📊 ADMIN TESTS SUMMARY")
        print("=" * 80)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed / (passed + failed) * 100):.1f}%")
        
        if failed > 0:
            print("\n🔍 Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['message']}")
        
        return failed == 0


if __name__ == "__main__":
    tester = AdminEndpointTester()
    
    # Run admin tests
    success = tester.run_admin_tests()
    
    if success:
        print("\n🎉 All admin tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some admin tests failed!")
        sys.exit(1)