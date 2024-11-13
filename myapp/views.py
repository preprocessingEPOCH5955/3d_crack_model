from django.shortcuts import render,HttpResponse, HttpResponseRedirect, get_object_or_404
import subprocess
from myProject.settings import BASE_DIR
from django.urls import reverse
import vtk
from django.views.decorators.csrf import csrf_exempt
from .models import *
global session, admin1, user_email,building_id,face,cur_data
session = False
cur_data = []
admin1 = False
user_email = ""
building_id = 1
face = 'Front'

red_coordinates = []
mapi = []

# Create your views here.
def e404(request):
    return render(request , '404.html')

def side_btn(request,side_id):
    global face
    if side_id == 1:
        face = 'Front'
    elif side_id == 2:
        face = 'Back'
    elif side_id == 3:
        face = "Left"
    elif side_id == 4:
        face = "Right"
    print(face, "new face")
    return HttpResponseRedirect(reverse("visualise"))
def reset(request):
    global building_id,cur_data
    building_id+=1
    cur_data = []
    print(building_id, "new building id")
    return HttpResponseRedirect(reverse("visualise"))

@csrf_exempt
def update_coordinates(request):
    global red_coordinates, mapi,building_id,user_email,cur_data
    if request.method == 'POST':
        crack_coordinates = request.POST.get('crack_coordinates') 
        try:
            log = request.POST.get('log')
            lat = request.POST.get('lat')
            lid = request.POST.get('lid')
            res = request.POST.get('result')
            print(log,lat,lid,res)
            new_cur = {
                'log':log,'lat':lat,'lid':lid,'res':res,'face':face
            }
            cur_data.append(new_cur)
            user_id = Signup_form.objects.get(email = user_email)
            print(user_id)
            try:
                obj = project_data.objects.create(user = user_id, lon = log, lat = lat, lid = lid, result = res, face = face, building_id = building_id)
                obj.save()
            except Exception as e:
                print("Data is not saved!",e)
            mapi = [log, lat, lid,res]
        except Exception as e:
            print(f"error as {e}")
        print(crack_coordinates)
        if crack_coordinates:
            try:
                from ast import literal_eval
                crack_coordinates = literal_eval(crack_coordinates)  # Convert string to list
                print("step1 ", crack_coordinates)

                # Append formatted coordinates to the global list
                red_coordinates.append(crack_coordinates)
                # print("now list is ",red_coordinates)
                return HttpResponse("Crack coordinates sent to server successfully")
            except (ValueError, SyntaxError) as e:
                return HttpResponse(f"Error processing coordinates: {e}")
        else:
            return HttpResponse("Wrong data format sent from Raspberry Pi.")
    
    return HttpResponse("Invalid request method.")
        
def reset_coordinates(request):
    global red_coordinates
    red_coordinates = []
    return HttpResponse("report reset now.")


# from django.shortcuts import render

def visualise_results(request):
    global user_email, red_coordinates, mapi,cur_data
    print (cur_data, red_coordinates)
   
    try:
        user = Signup_form.objects.get(email=user_email)
        print("user name ", user.firstname + " " + user.lastname)
    except:
        return HttpResponseRedirect(reverse("login"))
    
    
    try:
        projects = []
        user_data  = user
        print(f" user: {user_data.firstname}")
        # all_projects = project_data.objects.filter(user = user_data)
        # print(all_projects)
    except Signup_form.DoesNotExist:
        return HttpResponseRedirect(reverse("login"))
        projects = []
    all_data = []
    current_building_id = None
    current_group = []
    try:
        for project in cur_data:
                record = project
                
                print( "<<<<<<< cur data", record)

                data_point = {
                    # 'project_name': user_data.project_name,
                    # 'user_id': record.user.id ,
                    'longitude': record["log"],
                    'latitude': record["lat"],
                    'lidar': record["lid"],
                    'cracks': record["res"],
                    'face': record["face"],
                    'building_id': building_id,
                }
                
                all_data.append(data_point)
        print(all_data)
        

    except Exception as e:
        print(f"There was an error: {e}")
        all_data = []

    
    list = [li for li in red_coordinates]
    print(list)

    # Create a range for the grid
    grid_size = 4  # You can change this if you need a different size
    range_grid = range(grid_size)
  
        
    matrix = [
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(1, 0), (1, 1), (1, 2), (1, 3)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(3, 0), (3, 1), (3, 2), (3, 3)],

    ]
    found_coordinates = []
    boxes = {}
    box_counter = 1

    for i, row in enumerate(matrix):
        for j, coord in enumerate(row):
            if coord in red_coordinates:
                found_string = f"Red coordinate {coord} found at matrix[{i}][{j}]"
                found_coordinates.append(found_string)
                box_name = f'box{box_counter}'
                boxes[box_name] = 'red'
            
            box_counter += 1
    project_name = None
    # return HttpResponse (all_data)
    print("final data : ",all_data)
    return render(request, 'visualize.html', {'data': all_data, 'range_grid': range_grid,'red_coordinates': red_coordinates,'color':'custom-color', 'value':1,'boxes':boxes,'project_name':project_name})



def mymodel(request):

    # Create a reader to read the .obj file 
    reader = vtk.vtkOBJReader()
    reader.SetFileName("myapp\\static\\building_model.obj")
    reader.Update()

    # Create a mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Create an actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Apply shading properties to the actor (for material)
    actor.GetProperty().SetColor(1, 1, 1)  # Default to white if no colors are loaded
    actor.GetProperty().SetDiffuse(0.8)  # Diffuse reflection (how much light scatters)
    actor.GetProperty().SetSpecular(0.5)  # Specular reflection (how shiny the surface is)
    actor.GetProperty().SetSpecularPower(30)  # Shininess

    # Create a renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Add the actor to the scene
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.1, 0.1)  # Background color dark gray

    # Create a light source (to properly show material and textures)
    light = vtk.vtkLight()
    light.SetPosition(1, 1, 1)
    light.SetFocalPoint(0, 0, 0)
    renderer.AddLight(light)

    # Render and interact
    render_window.Render()
    render_window_interactor.Start()
    return HttpResponse("model loaded Successfully ")


def mymodel_new(request):
    return render(request, 'load_model_page.html')


def login(request):
    global admin1,session,user_email
    if session:
        return HttpResponseRedirect(reverse('home'))
    elif request.method =="POST":
        email = request.POST['email']
        password = request.POST['password']
        print('email',email)
        print('password',password)
        obj  =  Signup_form.objects.get(email = email)
        try:
            if email == obj.email:
                    if password == obj.password:
                        session = True
                        user_email = email
                        if obj.email == "rizwan@gmail.com":
                            admin1 = True
                            return HttpResponseRedirect(reverse('admin1'))
                        else:
                            return HttpResponseRedirect(reverse('get_started'))
                    else:
                        msg2 = "Password or User Email does not Matched"
                        # return render(request, 'login.html',{"msg2":msg2})         
                        return render (request, 'login.html',{'s':session,"msg2":msg2})
        except:
            msg2 = "Password or User Email does not Matched"
            return render(request, 'login.html',{"msg2":msg2})         
    return render(request, 'login.html') 

def home1(request):
    global admin1, session
    return render (request, 'index.html',{"a":admin1, "s":session})

def about(request):
    global admin1, session
    return render (request, 'about.html',{'a':admin1, "s":session})
def logout(request):
    global session, admin1
    session =False
    admin1 =False
    reset(request)
    return HttpResponseRedirect(reverse("login"))

def get_started(request):
    global admin1, session
    print(admin1, session)
    if session:
        return render(request, 'start.html',{"s":session, "a":admin1})
    else:
        return HttpResponseRedirect (reverse("login"))

def report(request):
    return render(request, 'report.html')





def admin1(request):
    if admin1 == True:
        a = admin1

        try:
            data = Signup_form.objects.all()
            userData = []
            for i in data:
                userData.append(i)
        except Exception as e:
            print(f"{e}")
        return render (request, 'admin1.html',{'s':session, 'a':a,"data":userData})  

      
    else:
        return HttpResponseRedirect(reverse('login'))
def user_data(request, id):
    pass

def user_projects_view(request, id):
    # return HttpResponse("Good")
    global user_email
    try:
        projects = []
        user_data = Signup_form.objects.get(id=id)
        print(f" user: {user_data.firstname}")
        all_projects = project_data.objects.filter(user = user_data)
        print(all_projects)
    except Signup_form.DoesNotExist:
        return HttpResponseRedirect(reverse("login"))
        projects = []
    all_data = []
    current_building_id = None
    current_group = []
    try:
        for project in all_projects:
                print(f"Processing data for project: {user_data.project_name}")
                record = project
                for i in range(len(record.lon)):
                    data_point = {
                        'project_name': user_data.project_name,
                        'user_id': record.user.id ,
                        'longitude': record.lon,
                        'latitude': record.lat,
                        'lidar': record.lid,
                        'cracks': record.result,
                        'face': record.face,
                        'building_id': record.building_id,
                    }
                    if current_building_id is None or current_building_id == record.building_id:
                        current_group.append(data_point)
                    else:
                        all_data.append(current_group)
                        current_group = [data_point]
                    current_building_id = record.building_id
        if current_group:
            all_data.append(current_group)
        print(all_data)

    except Exception as e:
        print(f"There was an error: {e}")
        all_data = []
    return render(request, 'usr_admin.html', {'data': all_data})
    # return HttpResponse(all_data)



def signup(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        emial = request.POST['mail']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        project_name = request.POST['project_name']
        print('firstname',firstname)
        print('lastname',lastname)
        print('emial',emial)
        print("project Name :", project_name)
        print('password',password)
        print('confirm_password',confirm_password)

        if password != confirm_password:
            msg1 = "Password & Confirm Password are not matched "
            return render(request, 'signup.html',{"msg1":msg1})  
        try:
            data = Signup_form.objects.create(firstname = firstname, lastname = lastname, email = emial, password = password, project_name = project_name)
            data.save()
        except:
            msg = 'Please Enter different Email, This Email Already Exist'
            return render(request, 'signup.html',{"msg":msg})  
        return HttpResponseRedirect(reverse("login"))

#         firstname 
# lastname 
# email
# password

    return render(request, 'signup.html')    
