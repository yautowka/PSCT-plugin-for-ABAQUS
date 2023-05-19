from abaqus import *
from abaqusConstants import *
import __main__
from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *

path_import = 'D:/VKR_PSCT/Calculations/Static_Rate_Depend/40_375'
path_export = 'D:/VKR_PSCT/TXT/Static_Rate_40_375'
names = os.listdir(path_import)

step = 0

for name in names:
    filename, file_extension = os.path.splitext(name)
    if file_extension == '.odb':
        temp_odb_view = session.openOdb(name=path_import + '/' + name)
        session.viewports['Viewport: 1'].setValues(displayedObject=temp_odb_view)
        odb = session.odbs[path_import + '/' + name]
        # frames = list(range(0, odb.steps['Step-1'].frames[-1].frameId - 1))
        if not os.path.isdir(path_export + '/' + filename):
            os.makedirs(path_export + '/' + filename)
        # os.mkdir(path_export + '/' + filename)
        lastFrame = len(odb.steps['Step-1'].frames)
        for frame in range(0, lastFrame):
            session.viewports['Viewport: 1'].odbDisplay.setFrame(step=step, frame=frame)
            session.fieldReportOptions.setValues(printTotal=OFF, printMinMax=OFF)
            session.writeFieldReport(
                fileName=path_export + '/' + filename + '/' + filename + '_' + str(frame) + '.txt',
                append=OFF,
                sortItem='Nodal Label', odb=odb, step=step, frame=frame, outputPosition=NODAL,
                variable=(
                    ('COORD', NODAL,
                     ((COMPONENT, 'COOR1'), (COMPONENT, 'COOR2'), (COMPONENT, 'COOR3'),)),
                    ('U', NODAL, ((COMPONENT, 'U1'), (COMPONENT, 'U2'), (COMPONENT, 'U3'),)),
                    ('RF', NODAL, ((COMPONENT, 'RF1'), (COMPONENT, 'RF2'), (COMPONENT, 'RF3'),)),
                    ('S', INTEGRATION_POINT, (
                        (INVARIANT, 'Mises'), (COMPONENT, 'S11'), (COMPONENT, 'S22'),
                        (COMPONENT, 'S33'),
                        (COMPONENT, 'S12'), (COMPONENT, 'S13'), (COMPONENT, 'S23'),)),
                    ('PE', INTEGRATION_POINT, (
                        (COMPONENT, 'PE11'), (COMPONENT, 'PE22'), (COMPONENT, 'PE33'),
                        (COMPONENT, 'PE12'),
                        (COMPONENT, 'PE13'), (COMPONENT, 'PE23'),)),
                    ('PEEQ', INTEGRATION_POINT),
                ))
        odb.close()
