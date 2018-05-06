import math
from display import *

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 10 # edit this!

# lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
  a = calculate_ambient(ambient, areflect)
  d = calculate_diffuse(light, dreflect, normal)
  s = calculate_specular(light, sreflect, view, normal)
  color = []
  for i in range(0, 3):
    color.append(a[i] + d[i] + s[i])
  print color
  return limit_color(color)


def calculate_ambient(alight, areflect):
  a = []
  for i in range(0, 3):
    a.append(alight[i] * areflect[i])
  return limit_color(a)


def calculate_diffuse(light, dreflect, normal):
  d = []
  for i in range(0, 3):
    d.append(light[COLOR][i] * dreflect[i] * dot_product(normalize(normal), normalize(light[LOCATION])))
  return limit_color(d)


def calculate_specular(light, sreflect, view, normal):
  normal = normalize(normal)
  lightloc = normalize(light[LOCATION])
  view = normalize(view)
  if (dot_product(normal, lightloc) <= 0):
    return [0, 0, 0]
  else:
    s = []
    R = []
    NdL = 2 * dot_product(normal, lightloc)
    for i in range(0, 3):
      R.append(NdL * normal[i] - lightloc[i])
    cosa = dot_product(R, view)
    for i in range(0, 3):
      s.append(light[COLOR][i] * sreflect[i] * (cosa ** SPECULAR_EXP))
    return limit_color(s)


def limit_color(color):
  for i in range(0, 3):
    rgb = color[i]
    rgb = int(rgb)
    if (rgb < 0):
      rgb = 0
    elif (rgb > 255):
      rgb = 255
    color[i] = rgb
  return color


#vector functions
def normalize(vector):
  bot = ((vector[0] ** 2) + (vector[1] ** 2) + (vector[2] ** 2)) ** 0.5
  for i in range(0, 3):
    vector[i] = vector[i] / bot
  return vector


def dot_product(a, b):
  output = 0
  for i in range(0, 3):
    output += a[i] * b[i]
  return output


def calculate_normal(polygons, i):
  A = [0, 0, 0]
  B = [0, 0, 0]
  N = [0, 0, 0]

  A[0] = polygons[i+1][0] - polygons[i][0]
  A[1] = polygons[i+1][1] - polygons[i][1]
  A[2] = polygons[i+1][2] - polygons[i][2]

  B[0] = polygons[i+2][0] - polygons[i][0]
  B[1] = polygons[i+2][1] - polygons[i][1]
  B[2] = polygons[i+2][2] - polygons[i][2]

  N[0] = A[1] * B[2] - A[2] * B[1]
  N[1] = A[2] * B[0] - A[0] * B[2]
  N[2] = A[0] * B[1] - A[1] * B[0]

  return N