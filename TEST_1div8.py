# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
# nameOfModel = 'test'
#
# widthOfCompression = 0.015
# highOfCompression = 0.01
# depthOfCompression = 0.0550
#
# widthOfSample = 0.07
# highOfSample = 0.005
# depthOfSample = 0.05
#
# sizeOfMesh = 0.0005
#
# friction = ((0.2, ), )
#
# amplitudeAndTime = ((0.0, 0.0), (2.0, 0.0), (4.0,
#     0.0), (6.0, 0.0), (8.0, 0.0), (10.0, 0.0), (12.0, 0.0), (14.0, 0.0), (16.0,
#     0.0), (18.0, 0.0), (20.0, 0.0), (22.0, 0.0), (24.0, 0.0), (26.0, 0.0), (
#     28.0, 0.0), (30.0, 0.0), (32.0, 0.0), (34.0, 0.0), (36.0, 0.0), (38.0,
#     0.0), (40.0, 0.0), (42.0, 0.0), (44.0, 0.0), (46.0, 0.0), (48.0, 0.0), (
#     50.0, 0.0), (52.0, 0.0), (54.0, 0.0), (56.0, 0.0), (58.0, 0.0), (60.0,
#     0.0), (62.0, 0.0), (64.0, 0.0), (66.0, 0.0), (68.0, 0.0), (70.0, 0.0), (
#     72.0, 0.0), (74.0, 0.0), (76.0, 0.0), (78.0, 0.0), (80.0, 0.0), (82.0,
#     0.0), (84.0, 0.0), (86.0, 0.0), (88.0, 0.0), (90.0, 0.0), (92.0, 0.0), (
#     94.0, 0.0), (96.0, 0.0), (98.0, 0.0), (103.636, 0.0), (107.487,
#     0.1662382741), (109.84, 0.2587383547), (112.834, 0.3830424506), (116.471,
#     0.5257528119), (119.037, 0.6219573548), (122.032, 0.7367413358), (125.668,
#     0.8685184912), (129.733, 1.015513336), (133.797, 1.147988841), (137.005,
#     1.258027103), (140.642, 1.373691337), (143.636, 1.460226821), (146.631,
#     1.55302998), (150.267, 1.659575686), (152.406, 1.723499454), (156.257,
#     1.832435962), (159.465, 1.915480816), (161.818, 1.974507476), (165.027,
#     2.06093504), (167.807, 2.131068176), (170.16, 2.192757918), (172.941,
#     2.253118785), (174.941, 2.263118785), (176.941, 2.273118785), (178.941,
#     2.283118785), (180.941, 2.293118785), (182.941, 2.303118785), (184.941,
#     2.313118785), (186.941, 2.323118785), (188.941, 2.333118785), (190.941,
#     2.343118785))
# speed = 1

def create_model_for_psct(nameOfModel, widthOfCompression, highOfCompression, depthOfCompression, widthOfSample, highOfSample, depthOfSample, density, elasticParams, plasticParams, sizeOfMesh, friction, amplitudeAndTime, speed, initialIncrement, maxIncrement, maxNumIncrement, minIncrement, time):
    mdb.Model(nameOfModel) #create model with name==nameOfModel
    densityParams = ((density,),)
    #geometry
    mdb.models[nameOfModel].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models[nameOfModel].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
        widthOfCompression/2, 0.0))
    mdb.models[nameOfModel].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[2])
    mdb.models[nameOfModel].sketches['__profile__'].Line(point1=(widthOfCompression/2, 0.0),
        point2=(widthOfCompression/2, highOfCompression))
    mdb.models[nameOfModel].sketches['__profile__'].VerticalConstraint(addUndoState=
        False, entity=mdb.models[nameOfModel].sketches['__profile__'].geometry[3])
    mdb.models[nameOfModel].sketches['__profile__'].PerpendicularConstraint(
        addUndoState=False, entity1=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[2], entity2=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[3])
    mdb.models[nameOfModel].sketches['__profile__'].Line(point1=(widthOfCompression/2, highOfCompression),
        point2=(0.0, highOfCompression))
    mdb.models[nameOfModel].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[4])
    mdb.models[nameOfModel].sketches['__profile__'].PerpendicularConstraint(
        addUndoState=False, entity1=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[3], entity2=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[4])
    mdb.models[nameOfModel].sketches['__profile__'].Line(point1=(0.0, highOfCompression), point2=(
        0.0, 0.0))
    mdb.models[nameOfModel].sketches['__profile__'].VerticalConstraint(addUndoState=
        False, entity=mdb.models[nameOfModel].sketches['__profile__'].geometry[5])
    mdb.models[nameOfModel].sketches['__profile__'].PerpendicularConstraint(
        addUndoState=False, entity1=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[4], entity2=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[5])
    mdb.models[nameOfModel].Part(dimensionality=THREE_D, name='Anvil', type=
        ANALYTIC_RIGID_SURFACE)
    mdb.models[nameOfModel].parts['Anvil'].AnalyticRigidSurfExtrude(depth=depthOfCompression/2,
        sketch=mdb.models[nameOfModel].sketches['__profile__'])
    del mdb.models[nameOfModel].sketches['__profile__']



    #geometry sample
    mdb.models[nameOfModel].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models[nameOfModel].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
        widthOfSample/2, 0.0))
    mdb.models[nameOfModel].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[2])
    mdb.models[nameOfModel].sketches['__profile__'].Line(point1=(widthOfSample/2, 0.0), point2=
        (widthOfSample/2, -highOfSample/2))
    mdb.models[nameOfModel].sketches['__profile__'].VerticalConstraint(addUndoState=
        False, entity=mdb.models[nameOfModel].sketches['__profile__'].geometry[3])
    mdb.models[nameOfModel].sketches['__profile__'].PerpendicularConstraint(
        addUndoState=False, entity1=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[2], entity2=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[3])
    mdb.models[nameOfModel].sketches['__profile__'].Line(point1=(widthOfSample/2, -highOfSample/2),
        point2=(0.0, -highOfSample/2))
    mdb.models[nameOfModel].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[4])
    mdb.models[nameOfModel].sketches['__profile__'].PerpendicularConstraint(
        addUndoState=False, entity1=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[3], entity2=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[4])
    mdb.models[nameOfModel].sketches['__profile__'].Line(point1=(0.0, -highOfSample/2),
        point2=(0.0, 0.0))
    mdb.models[nameOfModel].sketches['__profile__'].VerticalConstraint(addUndoState=
        False, entity=mdb.models[nameOfModel].sketches['__profile__'].geometry[5])
    mdb.models[nameOfModel].sketches['__profile__'].PerpendicularConstraint(
        addUndoState=False, entity1=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[4], entity2=
        mdb.models[nameOfModel].sketches['__profile__'].geometry[5])
    mdb.models[nameOfModel].Part(dimensionality=THREE_D, name='Part-2', type=
        DEFORMABLE_BODY)
    mdb.models[nameOfModel].parts['Part-2'].BaseSolidExtrude(depth=depthOfSample/2, sketch=
        mdb.models[nameOfModel].sketches['__profile__'])
    del mdb.models[nameOfModel].sketches['__profile__']

    #reference point
    mdb.models[nameOfModel].parts['Anvil'].ReferencePoint(point=
        mdb.models[nameOfModel].parts['Anvil'].InterestingPoint(
        mdb.models[nameOfModel].parts['Anvil'].edges[1], MIDDLE))


    #materials of sample and applying them
    mdb.models[nameOfModel].Material(name='AL')
    mdb.models[nameOfModel].materials['AL'].Density(table=densityParams)
    mdb.models[nameOfModel].materials['AL'].Elastic(table=elasticParams)
    mdb.models[nameOfModel].materials['AL'].Plastic(rate=ON, table=plasticParams)
    mdb.models[nameOfModel].HomogeneousSolidSection(material='AL', name=
        'Section-1', thickness=None)
    mdb.models[nameOfModel].parts['Part-2'].Set(cells=
        mdb.models[nameOfModel].parts['Part-2'].cells.getSequenceFromMask(('[#1 ]',
        ), ), name='Set-1')
    mdb.models[nameOfModel].parts['Part-2'].SectionAssignment(offset=0.0,
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdb.models[nameOfModel].parts['Part-2'].sets['Set-1'], sectionName=
        'Section-1', thicknessAssignment=FROM_SECTION)

    # union
    mdb.models[nameOfModel].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models[nameOfModel].rootAssembly.Instance(dependent=ON, name='Anvil-1', part=
        mdb.models[nameOfModel].parts['Anvil'])
    mdb.models[nameOfModel].rootAssembly.Instance(dependent=ON, name='Part-2-1',
        part=mdb.models[nameOfModel].parts['Part-2'])


    #move
    mdb.models[nameOfModel].rootAssembly.translate(instanceList=('Anvil-1', ),
        vector=(0.0, 0.0, depthOfSample/4))

    # scale
    #mdb.models[nameOfModel].ExplicitDynamicsStep(improvedDtMethod=ON, massScaling=((
    #    SEMI_AUTOMATIC, MODEL, AT_BEGINNING, 10000.0, 0.0, None, 0, 0, 0.0, 0.0, 0,
    #   None), ), name='Step-1', previous='Initial')
    mdb.models[nameOfModel].StaticStep(initialInc=initialIncrement, maxInc=maxIncrement, 
        maxNumInc=maxNumIncrement, minInc=minIncrement, name='Step-1', previous='Initial', 
        timePeriod=time)

    #mesh
    mdb.models[nameOfModel].parts['Part-2'].seedPart(deviationFactor=0.1,
        minSizeFactor=0.1, size=sizeOfMesh)
    mdb.models[nameOfModel].parts['Part-2'].generateMesh()

    # surfaces and friction
    mdb.models[nameOfModel].rootAssembly.regenerate()
    mdb.models[nameOfModel].ContactProperty('IntProp-1')
    mdb.models[nameOfModel].interactionProperties['IntProp-1'].TangentialBehavior(
        dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, 
        formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, 
        pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, 
        table=((friction, ), ), temperatureDependency=OFF)
    mdb.models[nameOfModel].rootAssembly.Surface(name='m_Surf-1', 
        side1Faces=
        mdb.models[nameOfModel].rootAssembly.instances['Anvil-1'].faces.getSequenceFromMask(
        ('[#f ]', ), ))
    mdb.models[nameOfModel].rootAssembly.Surface(name='s_Surf-1', 
        side1Faces=
        mdb.models[nameOfModel].rootAssembly.instances['Part-2-1'].faces.getSequenceFromMask(
        ('[#1 ]', ), ))
    mdb.models[nameOfModel].SurfaceToSurfaceContactStd(adjustMethod=NONE, 
        clearanceRegion=None, createStepName='Initial', datumAxis=None, 
        initialClearance=OMIT, interactionProperty='IntProp-1', master=
        mdb.models[nameOfModel].rootAssembly.surfaces['m_Surf-1'], name=
        'Int-1', slave=
        mdb.models[nameOfModel].rootAssembly.surfaces['s_Surf-1'], 
        sliding=FINITE, thickness=ON)


    # speed
    mdb.models[nameOfModel].rootAssembly.Set(faces=
        mdb.models[nameOfModel].rootAssembly.instances['Part-2-1'].faces.getSequenceFromMask(
        ('[#8 ]', ), ), name='Set-1')
    mdb.models[nameOfModel].XsymmBC(createStepName='Initial', localCsys=
        None, name='BC-1', region=
        mdb.models[nameOfModel].rootAssembly.sets['Set-1'])
    mdb.models[nameOfModel].rootAssembly.Set(faces=
        mdb.models[nameOfModel].rootAssembly.instances['Part-2-1'].faces.getSequenceFromMask(
        ('[#4 ]', ), ), name='Set-2')
    mdb.models[nameOfModel].YsymmBC(createStepName='Initial', localCsys=
        None, name='BC-2', region=
        mdb.models[nameOfModel].rootAssembly.sets['Set-2'])
    mdb.models[nameOfModel].rootAssembly.Set(faces=
        mdb.models[nameOfModel].rootAssembly.instances['Part-2-1'].faces.getSequenceFromMask(
        ('[#10 ]', ), ), name='Set-3')
    mdb.models[nameOfModel].ZsymmBC(createStepName='Initial', localCsys=
        None, name='BC-3', region=
        mdb.models[nameOfModel].rootAssembly.sets['Set-3'])



    #amplitude and time
    mdb.models[nameOfModel].TabularAmplitude(data=amplitudeAndTime, name='Amp-1', smooth=SOLVER_DEFAULT, timeSpan=STEP)
    mdb.models[nameOfModel].rootAssembly.Set(name='Set-4', referencePoints=(
        mdb.models[nameOfModel].rootAssembly.instances['Anvil-1'].referencePoints[2],
        ))
    mdb.models[nameOfModel].DisplacementBC(amplitude='Amp-1', createStepName='Step-1'
        , distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'BC-4', region=mdb.models[nameOfModel].rootAssembly.sets['Set-4'], u1=0.0,
        u2=-speed, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0)
    mdb.models[nameOfModel].fieldOutputRequests['F-Output-1'].setValues(
        frequency=20, variables=('S', 'MISES', 'E', 'PE', 'PEEQ', 'PEMAG', 'LE', 
        'ER', 'U', 'RF', 'CF', 'COORD'))

