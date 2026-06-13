from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import JobRole, Skill, Tool, SalaryInsight, CareerGrowthPath, JobProcess
from .serializers import JobRoleSerializer, SkillSerializer, ToolSerializer, SalaryInsightSerializer

class JobRoleViewSet(viewsets.ModelViewSet):
    """
    Job role information and visualization
    """
    queryset = JobRole.objects.all()
    serializer_class = JobRoleSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def search(self, request):
        """
        Search for job roles
        """
        query = request.query_params.get('q', '')
        if query:
            jobs = JobRole.objects.filter(Q(job_name__icontains=query) | Q(description__icontains=query))
            serializer = JobRoleSerializer(jobs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Query parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def process(self, request, pk=None):
        """
        Get job process/workflow
        """
        job = self.get_object()
        try:
            process = job.process
            return Response(process.process_json, status=status.HTTP_200_OK)
        except JobProcess.DoesNotExist:
            return Response({'error': 'Process not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def skills(self, request, pk=None):
        """
        Get required skills for a job
        """
        job = self.get_object()
        skills = job.skills.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def tools(self, request, pk=None):
        """
        Get tools used in a job
        """
        job = self.get_object()
        tools = job.tools.all()
        serializer = ToolSerializer(tools, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def salary(self, request, pk=None):
        """
        Get salary insights for a job
        """
        job = self.get_object()
        try:
            salary = job.salary
            serializer = SalaryInsightSerializer(salary)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SalaryInsight.DoesNotExist:
            return Response({'error': 'Salary info not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def career_growth(self, request, pk=None):
        """
        Get career growth path
        """
        job = self.get_object()
        try:
            growth = job.growth_path
            return Response(growth.growth_json, status=status.HTTP_200_OK)
        except CareerGrowthPath.DoesNotExist:
            return Response({'error': 'Growth path not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def full_details(self, request, pk=None):
        """
        Get complete job details
        """
        job = self.get_object()
        data = JobRoleSerializer(job).data
        data['skills'] = SkillSerializer(job.skills.all(), many=True).data
        data['tools'] = ToolSerializer(job.tools.all(), many=True).data
        
        try:
            data['process'] = job.process.process_json
        except:
            data['process'] = []
        
        try:
            data['salary'] = SalaryInsightSerializer(job.salary).data
        except:
            data['salary'] = {}
        
        try:
            data['career_growth'] = job.growth_path.growth_json
        except:
            data['career_growth'] = []
        
        return Response(data, status=status.HTTP_200_OK)
