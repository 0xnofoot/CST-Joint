import os

from core import global_var

resource_dir = global_var.resource_dir
vb_dir = os.path.join(resource_dir, "cst", "vb")


# 利用相应的template vb脚本初始化工程
def initial_template(modeler, template_file_name, freq_low, freq_high):
    path = os.path.join(vb_dir, template_file_name)
    with open(path, mode="r", encoding="utf-8") as f:
        s_command = f.read()
        s_command = s_command.replace("{$freq_low}", str(freq_low))
        s_command = s_command.replace("{$freq_high}", str(freq_high))
        modeler.add_to_history(template_file_name, s_command)


# 在CST中保存结构参数
def save_params(modeler, name, value):
    s_command = "MakeSureParameterExists(\"{$name}\", \"{$value}\")"
    s_command = s_command.replace("{$name}", name)
    s_command = s_command.replace("{$value}", str(value))

    modeler.add_to_history("StoreParameter_" + name, s_command)


# 定义材料
def define_material(modeler, name, epsilon, mu, tand, folder, color):
    path = os.path.join(vb_dir, "define_material")
    with open(path, mode="r", encoding="utf-8") as f:
        s_command = f.read()
        s_command = s_command.replace("{$name}", name)
        s_command = s_command.replace("{$folder}", folder)
        s_command = s_command.replace("{$epsilon}", str(epsilon))
        s_command = s_command.replace("{$mu}", str(mu))
        s_command = s_command.replace("{$tand}", str(tand))
        s_command = s_command.replace("{$color_h}", str(color[0]))
        s_command = s_command.replace("{$color_s}", str(color[1]))
        s_command = s_command.replace("{$color_v}", str(color[2]))

        modeler.add_to_history("define_material_" + name, s_command)


# 加载vb脚本中已有的材料
def load_material(modeler, name):
    path = os.path.join(vb_dir, "materials", name)
    with open(path, mode="r", encoding="utf-8") as f:
        s_command = f.read()
        modeler.add_to_history("load_material_" + name, s_command)


# 创建一个brick
def create_brick(modeler, name, material, x1_range, x2_range, y1_range, y2_range,
                 z1_range, z2_range, component):
    path = os.path.join(vb_dir, "create_brick")
    with open(path, mode="r", encoding="utf-8") as f:
        s_command = f.read()
        s_command = s_command.replace("{$name}", name)
        s_command = s_command.replace("{$material}", material)
        s_command = s_command.replace("{$x1_range}", str(x1_range))
        s_command = s_command.replace("{$x2_range}", str(x2_range))
        s_command = s_command.replace("{$y1_range}", str(y1_range))
        s_command = s_command.replace("{$y2_range}", str(y2_range))
        s_command = s_command.replace("{$z1_range}", str(z1_range))
        s_command = s_command.replace("{$z2_range}", str(z2_range))
        s_command = s_command.replace("{$component}", component)

        modeler.add_to_history("create_brick_" + name, s_command)


def delete_solid(modeler, component, solid):
    solid = component + ":" + solid
    s_command = "Solid.Delete\"{$solid}\""
    s_command = s_command.replace("{$solid}", solid)
    modeler.add_to_history("delete solid", s_command)


# 缩放视角到适合大小，和在CST里面按空格是一个效果
def zoom_to_structure(modeler):
    s_command = "Plot.ZoomToStructure"
    modeler.add_to_history("ZoomToStructure", s_command)


def bool_add(modeler, component1, solid1, component2, solid2):
    solid1 = component1 + ":" + solid1
    solid2 = component2 + ":" + solid2
    s_command = "Solid.Add \"{$solid1}\", \"{$solid2}\""
    s_command = s_command.replace("{$solid1}", solid1)
    s_command = s_command.replace("{$solid2}", solid2)
    modeler.add_to_history("bool_add", s_command)


def bool_subtract(modeler, component1, solid1, component2, solid2):
    solid1 = component1 + ":" + solid1
    solid2 = component2 + ":" + solid2
    s_command = "Solid.Subtract \"{$solid1}\", \"{$solid2}\""
    s_command = s_command.replace("{$solid1}", solid1)
    s_command = s_command.replace("{$solid2}", solid2)
    modeler.add_to_history("bool_subtract", s_command)


def translate(modeler, component, name, vector, copy, merge):
    name = component + ":" + name
    path = os.path.join(vb_dir, "translate")
    with open(path, mode="r", encoding="utf-8") as f:
        s_command = f.read()
        s_command = s_command.replace("{$name}", name)
        s_command = s_command.replace("{$v1}", str(vector[0]))
        s_command = s_command.replace("{$v2}", str(vector[1]))
        s_command = s_command.replace("{$v3}", str(vector[2]))
        if copy is True:
            s_command = s_command.replace("{$copy}", "True")
        else:
            s_command = s_command.replace("{$copy}", "False")

        if merge is True:
            s_command = s_command.replace("{$merge}", "True")
        else:
            s_command = s_command.replace("{$merge}", "False")
        modeler.add_to_history("translate", s_command)


def rotate(modeler, component, name, center, angle, copy, merge):
    name = component + ":" + name
    path = os.path.join(vb_dir, "rotate")
    with open(path, mode="r", encoding="utf-8") as f:
        s_command = f.read()
        s_command = s_command.replace("{$name}", name)
        s_command = s_command.replace("{$c1}", str(center[0]))
        s_command = s_command.replace("{$c2}", str(center[1]))
        s_command = s_command.replace("{$c3}", str(center[2]))
        s_command = s_command.replace("{$a1}", str(angle[0]))
        s_command = s_command.replace("{$a2}", str(angle[1]))
        s_command = s_command.replace("{$a3}", str(angle[2]))
        if copy is True:
            s_command = s_command.replace("{$copy}", "True")
        else:
            s_command = s_command.replace("{$copy}", "False")

        if merge is True:
            s_command = s_command.replace("{$merge}", "True")
        else:
            s_command = s_command.replace("{$merge}", "False")
        modeler.add_to_history("rotate", s_command)


def mirror(modeler, component, name, center, plane, copy, merge):
    name = component + ":" + name
    path = os.path.join(vb_dir, "mirror")
    with open(path, mode="r", encoding="utf-8") as f:
        s_command = f.read()
        s_command = s_command.replace("{$name}", name)
        s_command = s_command.replace("{$c1}", str(center[0]))
        s_command = s_command.replace("{$c2}", str(center[1]))
        s_command = s_command.replace("{$c3}", str(center[2]))
        s_command = s_command.replace("{$p1}", str(plane[0]))
        s_command = s_command.replace("{$p2}", str(plane[1]))
        s_command = s_command.replace("{$p3}", str(plane[2]))
        if copy is True:
            s_command = s_command.replace("{$copy}", "True")
        else:
            s_command = s_command.replace("{$copy}", "False")

        if merge is True:
            s_command = s_command.replace("{$merge}", "True")
        else:
            s_command = s_command.replace("{$merge}", "False")
        modeler.add_to_history("mirror", s_command)


def rename(modeler, component, name, new_name):
    name = component + ":" + name
    s_command = "Solid.Rename \"{$name}\", \"{$new_name}\""
    s_command = s_command.replace("{$name}", name)
    s_command = s_command.replace("{$new_name}", new_name)
    modeler.add_to_history('rename', s_command)


def solver_add_port(modeler, port_name, mode):
    path = os.path.join(vb_dir, "solver_add_port")
    with open(path, mode="r", encoding="utf-8") as f:
        s_command = f.read()
        s_command = s_command.replace("{$name}", port_name)
        s_command = s_command.replace("{$mode}", mode)
        modeler.add_to_history("solver_add_port", s_command)


def run_solver(modeler):
    isComplete = modeler.run_solver()
    return isComplete


def boundary(modeler, Xmin, Xmax, Ymin, Ymax, Zmin, Zmax):
    path = os.path.join(vb_dir, "boundary")
    with open(path, mode="r", encoding="utf-8") as f:
        s_command = f.read()
        s_command = s_command.replace("{$Xmin}", Xmin)
        s_command = s_command.replace("{$Xmax}", Xmax)
        s_command = s_command.replace("{$Ymin}", Ymin)
        s_command = s_command.replace("{$Ymax}", Ymax)
        s_command = s_command.replace("{$Zmin}", Zmin)
        s_command = s_command.replace("{$Zmax}", Zmax)
        modeler.add_to_history("define boundary", s_command)
