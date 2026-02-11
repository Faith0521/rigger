//Maya ASCII 2018ff09 scene
//Name: DX11.ma
//Last modified: Fri, Dec 20, 2019 12:16:21 PM
//Codeset: 936
requires maya "2018ff09";
requires -nodeType "dx11Shader" "dx11Shader" "1.0";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t pal;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201903222215-65bada0e52";
fileInfo "osv" "Microsoft Windows 8 Business Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "719DB8C8-45D0-83CC-02A8-35A97A07ED28";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 11.948912322499915 29.316764506941176 29.874412041219802 ;
	setAttr ".r" -type "double3" -42.338352729603479 21.800000000000551 0 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "BC5155AF-4FB2-E6F4-9E4A-A59A50E77172";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 43.528492756524557;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "58D8BE93-435C-9F0C-BBD2-3DA4D2EEB371";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "BB8B9E7C-4556-9081-2D8D-DCA64E8F8B21";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "695309A5-48E0-18B8-3560-3599A179A6F5";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "CEB6FEC4-4D55-37B1-64F1-85AAB69E3C71";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "D2A7E4F8-42B9-A713-ADCD-408C637FE1EB";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "F785B656-491B-C0AF-7A55-E4A9125E3333";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode materialInfo -n "materialInfo14";
	rename -uid "BF67E7A4-45C5-2CFA-6AD2-42B5B567C42C";
createNode shadingEngine -n "dx11Shader8SG";
	rename -uid "543AF801-4634-35BA-B232-C08180F21B64";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "556AD7F1-47B0-0645-728F-529AB90BD41C";
	setAttr -s 7 ".lnk";
	setAttr -s 3 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "E539CC7D-4A6F-41D8-B68E-51AB167E08F0";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "FC3ACCE9-4F72-7664-0EF1-8BB7280051C9";
createNode displayLayerManager -n "layerManager";
	rename -uid "25DB7ABA-4464-0C94-D6F4-1498CAA0AE33";
createNode displayLayer -n "defaultLayer";
	rename -uid "AA22823F-47A0-36AD-E49F-C5B667CA01B6";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "A19C9414-498B-D852-5F8F-8A9C200A44E5";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "8E4E012B-4F1D-9A1C-6CAB-F8891410CE57";
	setAttr ".g" yes;
createNode place2dTexture -n "face_dx11_wrinkle_normal_place2dTexture";
	rename -uid "41FBACD2-4C03-35C5-2A6A-70A3B2884183";
createNode place2dTexture -n "face_dx11_wrinkle_color_place2dTexture";
	rename -uid "2366EC14-4AB1-1E55-AB51-2BB90EB93923";
createNode place2dTexture -n "face_dx11_maskMap4_place2dTexture";
	rename -uid "9EA07816-4944-C019-1AA8-E19CA50FCB71";
createNode place2dTexture -n "face_dx11_maskMap3_place2dTexture";
	rename -uid "973B8760-43CB-34C7-5D6A-D994ACC507DF";
createNode place2dTexture -n "face_dx11_maskMap2_place2dTexture";
	rename -uid "E73B6F55-4655-B434-74BC-659FA086F63F";
createNode place2dTexture -n "face_dx11_maskMap1_place2dTexture";
	rename -uid "DC7695F1-4BFE-353F-5464-888AF7669DC1";
createNode file -n "face_dx11_wrinkle_normal";
	rename -uid "8B9B1BCB-4AA5-047F-9B05-BE8691403A73";
	setAttr ".cs" -type "string" "sRGB";
createNode file -n "face_dx11_wrinkle_color";
	rename -uid "8A5441E2-40FF-A723-7F87-C381589236EB";
	setAttr ".cs" -type "string" "sRGB";
createNode file -n "face_dx11_normal_map";
	rename -uid "A19EEBCF-41E4-69D8-DB01-069F914C2501";
	setAttr ".cs" -type "string" "sRGB";
createNode file -n "face_dx11_maskMap4";
	rename -uid "BD795B3F-4174-0470-28BE-67A7B68E7CA7";
	setAttr ".ftn" -type "string" "I:/proj/mopian_immortal_epi/syncData/workgroup/RIG_WorkGrp/ExternalTeam/DX11/T_wrinkle_Mask_04_2048.tga";
	setAttr ".cs" -type "string" "sRGB";
createNode file -n "face_dx11_maskMap3";
	rename -uid "07F8E389-4300-9A39-EDDD-CDBD485619A0";
	setAttr ".ftn" -type "string" "I:/proj/mopian_immortal_epi/syncData/workgroup/RIG_WorkGrp/ExternalTeam/DX11/T_wrinkle_Mask_03_2048.tga";
	setAttr ".cs" -type "string" "sRGB";
createNode file -n "face_dx11_maskMap2";
	rename -uid "A7E8F70A-483B-5569-AD21-44B0FD94B993";
	setAttr ".ftn" -type "string" "I:/proj/mopian_immortal_epi/syncData/workgroup/RIG_WorkGrp/ExternalTeam/DX11/T_wrinkle_Mask_02_2048.tga";
	setAttr ".cs" -type "string" "sRGB";
createNode file -n "face_dx11_maskMap1";
	rename -uid "4EDBC157-48AD-B5ED-EDF4-DAA2DEFD6510";
	setAttr ".ftn" -type "string" "I:/proj/mopian_immortal_epi/syncData/workgroup/RIG_WorkGrp/ExternalTeam/DX11/T_wrinkle_Mask_01_2048.tga";
	setAttr ".cs" -type "string" "sRGB";
createNode file -n "face_dx11_diffuse_map";
	rename -uid "12326E58-47FD-72DC-4CA1-659905DDC0D7";
	setAttr ".cs" -type "string" "sRGB";
createNode dx11Shader -n "SkinShader";
	rename -uid "3C847A4A-4B6B-F8E4-8C6D-40BEA1DFEC51";
	addAttr -s false -is true -ci true -k true -sn "te" -ln "techniqueEnum" -nn "Technique" 
		-ct "HW_shader_parameter" -min 0 -max 2 -en "SkinShader" -at "enum";
	addAttr -ci true -sn "Light_0_use_implicit_lighting" -ln "Light_0_use_implicit_lighting" 
		-ct "HW_shader_parameter" -dv 1 -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "Light_0_connected_light" -ln "Light_0_connected_light" 
		-ct "HW_shader_parameter" -at "message";
	addAttr -ci true -sn "Light_1_use_implicit_lighting" -ln "Light_1_use_implicit_lighting" 
		-ct "HW_shader_parameter" -dv 1 -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "Light_1_connected_light" -ln "Light_1_connected_light" 
		-ct "HW_shader_parameter" -at "message";
	addAttr -ci true -sn "Light_2_use_implicit_lighting" -ln "Light_2_use_implicit_lighting" 
		-ct "HW_shader_parameter" -dv 1 -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "Light_2_connected_light" -ln "Light_2_connected_light" 
		-ct "HW_shader_parameter" -at "message";
	addAttr -is true -ci true -h true -sn "SuperFilterTaps_Name" -ln "SuperFilterTaps_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "SuperFilterTaps_Type" -ln "SuperFilterTaps_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "SuperFilterTaps" -ln "SuperFilterTaps" -ct "HW_shader_parameter" 
		-at "float2" -nc 2;
	addAttr -is true -ci true -sn "SuperFilterTapsX" -ln "SuperFilterTapsX" -ct "HW_shader_parameter" 
		-dv 0.48207607865333557 -smn 0 -smx 1 -at "float" -p "SuperFilterTaps";
	addAttr -is true -ci true -sn "SuperFilterTapsY" -ln "SuperFilterTapsY" -ct "HW_shader_parameter" 
		-dv -0.32157996296882629 -smn 0 -smx 1 -at "float" -p "SuperFilterTaps";
	addAttr -is true -ci true -h true -sn "shadowMapTexelSize_Name" -ln "shadowMapTexelSize_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "shadowMapTexelSize_Type" -ln "shadowMapTexelSize_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "shadowMapTexelSize" -ln "shadowMapTexelSize" 
		-ct "HW_shader_parameter" -dv 0.0019531298894435167 -smn 0 -smx 1 -at "float";
	addAttr -is true -ci true -h true -sn "LinearSpaceLighting_Name" -ln "LinearSpaceLighting_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "LinearSpaceLighting_Type" -ln "LinearSpaceLighting_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "LinearSpaceLighting" -ln "LinearSpaceLighting" 
		-nn "Linear Space Lighting" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "UseShadows_Name" -ln "UseShadows_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "UseShadows_Type" -ln "UseShadows_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "UseShadows" -ln "UseShadows" -nn "Shadows" 
		-ct "HW_shader_parameter" -dv 1 -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "shadowMultiplier_Name" -ln "shadowMultiplier_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "shadowMultiplier_Type" -ln "shadowMultiplier_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "shadowMultiplier" -ln "shadowMultiplier" 
		-nn "Shadow Strength" -ct "HW_shader_parameter" -dv 1 -min 0 -max 1 -at "float";
	addAttr -is true -ci true -h true -sn "IsSwatchRender_Name" -ln "IsSwatchRender_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "IsSwatchRender_Type" -ln "IsSwatchRender_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "IsSwatchRender" -ln "IsSwatchRender" -ct "HW_shader_parameter" 
		-min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "shadowDepthBias_Name" -ln "shadowDepthBias_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "shadowDepthBias_Type" -ln "shadowDepthBias_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "shadowDepthBias" -ln "shadowDepthBias" -nn "Shadow Bias" 
		-ct "HW_shader_parameter" -dv 0.0099999997764825821 -min 0 -smx 10 -at "float";
	addAttr -is true -ci true -h true -sn "MayaFullScreenGamma_Name" -ln "MayaFullScreenGamma_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "MayaFullScreenGamma_Type" -ln "MayaFullScreenGamma_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "MayaFullScreenGamma" -ln "MayaFullScreenGamma" 
		-ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "flipBackfaceNormals_Name" -ln "flipBackfaceNormals_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "flipBackfaceNormals_Type" -ln "flipBackfaceNormals_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "flipBackfaceNormals" -ln "flipBackfaceNormals" 
		-nn "Double Sided Lighting" -ct "HW_shader_parameter" -dv 1 -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "light0Enable_Name" -ln "light0Enable_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light0Enable_Type" -ln "light0Enable_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light0Enable" -ln "light0Enable" -nn "Enable Light 0" 
		-ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "light0Type_Name" -ln "light0Type_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "light0Type_Type" -ln "light0Type_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "light0Type" -ln "light0Type" -nn "Light 0 Type" 
		-ct "HW_shader_parameter" -dv 2 -min 0 -max 5 -smn 0 -smx 1 -en "None:Default:Spot:Point:Directional:Ambient" 
		-at "enum";
	addAttr -is true -ci true -h true -sn "light0Pos_Name" -ln "light0Pos_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "light0Pos_Type" -ln "light0Pos_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "light0Pos" -ln "light0Pos" -nn "Light 0 Position" 
		-ct "HW_shader_parameter" -at "matrix";
	addAttr -is true -ci true -h true -sn "light0Color_Name" -ln "light0Color_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light0Color_Type" -ln "light0Color_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -k true -sn "light0Color" -ln "light0Color" -nn "Light 0 Color" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "light0ColorR" -ln "light0ColorR" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "light0Color";
	addAttr -is true -ci true -sn "light0ColorG" -ln "light0ColorG" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "light0Color";
	addAttr -is true -ci true -sn "light0ColorB" -ln "light0ColorB" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "light0Color";
	addAttr -is true -ci true -h true -sn "light0Intensity_Name" -ln "light0Intensity_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light0Intensity_Type" -ln "light0Intensity_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light0Intensity" -ln "light0Intensity" -nn "Light 0 Intensity" 
		-ct "HW_shader_parameter" -dv 1 -min 0 -max 99999 -smn 0 -smx 1 -at "float";
	addAttr -is true -ci true -h true -sn "light0Dir_Name" -ln "light0Dir_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "light0Dir_Type" -ln "light0Dir_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "light0Dir" -ln "light0Dir" -nn "Light 0 Direction" 
		-ct "HW_shader_parameter" -at "matrix";
	addAttr -is true -ci true -h true -sn "light0ConeAngle_Name" -ln "light0ConeAngle_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light0ConeAngle_Type" -ln "light0ConeAngle_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light0ConeAngle" -ln "light0ConeAngle" -nn "Light 0 Cone Angle" 
		-ct "HW_shader_parameter" -dv 0.46000000834465027 -min 0 -max 1.5707962512969971 
		-at "float";
	addAttr -is true -ci true -h true -sn "light0FallOff_Name" -ln "light0FallOff_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light0FallOff_Type" -ln "light0FallOff_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light0FallOff" -ln "light0FallOff" -nn "Light 0 Penumbra Angle" 
		-ct "HW_shader_parameter" -dv 0.69999998807907104 -min 0 -max 1.5707962512969971 
		-at "float";
	addAttr -is true -ci true -h true -sn "light0AttenScale_Name" -ln "light0AttenScale_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light0AttenScale_Type" -ln "light0AttenScale_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light0AttenScale" -ln "light0AttenScale" 
		-nn "Light 0 Decay" -ct "HW_shader_parameter" -min 0 -max 99999 -smn 0 -smx 1 -at "float";
	addAttr -is true -ci true -h true -sn "light0ShadowOn_Name" -ln "light0ShadowOn_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light0ShadowOn_Type" -ln "light0ShadowOn_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light0ShadowOn" -ln "light0ShadowOn" -nn "Light 0 Casts Shadow" 
		-ct "HW_shader_parameter" -dv 1 -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "light1Enable_Name" -ln "light1Enable_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light1Enable_Type" -ln "light1Enable_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light1Enable" -ln "light1Enable" -nn "Enable Light 1" 
		-ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "light1Type_Name" -ln "light1Type_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "light1Type_Type" -ln "light1Type_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "light1Type" -ln "light1Type" -nn "Light 1 Type" 
		-ct "HW_shader_parameter" -dv 2 -min 0 -max 5 -smn 0 -smx 1 -en "None:Default:Spot:Point:Directional:Ambient" 
		-at "enum";
	addAttr -is true -ci true -h true -sn "light1Pos_Name" -ln "light1Pos_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "light1Pos_Type" -ln "light1Pos_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "light1Pos" -ln "light1Pos" -nn "Light 1 Position" 
		-ct "HW_shader_parameter" -at "matrix";
	addAttr -is true -ci true -h true -sn "light1Color_Name" -ln "light1Color_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light1Color_Type" -ln "light1Color_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -k true -sn "light1Color" -ln "light1Color" -nn "Light 1 Color" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "light1ColorR" -ln "light1ColorR" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "light1Color";
	addAttr -is true -ci true -sn "light1ColorG" -ln "light1ColorG" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "light1Color";
	addAttr -is true -ci true -sn "light1ColorB" -ln "light1ColorB" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "light1Color";
	addAttr -is true -ci true -h true -sn "light1Intensity_Name" -ln "light1Intensity_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light1Intensity_Type" -ln "light1Intensity_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light1Intensity" -ln "light1Intensity" -nn "Light 1 Intensity" 
		-ct "HW_shader_parameter" -dv 1 -min 0 -max 99999 -smn 0 -smx 1 -at "float";
	addAttr -is true -ci true -h true -sn "light1Dir_Name" -ln "light1Dir_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "light1Dir_Type" -ln "light1Dir_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "light1Dir" -ln "light1Dir" -nn "Light 1 Direction" 
		-ct "HW_shader_parameter" -at "matrix";
	addAttr -is true -ci true -h true -sn "light1ConeAngle_Name" -ln "light1ConeAngle_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light1ConeAngle_Type" -ln "light1ConeAngle_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light1ConeAngle" -ln "light1ConeAngle" -nn "Light 1 Cone Angle" 
		-ct "HW_shader_parameter" -dv 45 -min 0 -max 1.5707962512969971 -at "float";
	addAttr -is true -ci true -h true -sn "light1FallOff_Name" -ln "light1FallOff_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light1FallOff_Type" -ln "light1FallOff_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light1FallOff" -ln "light1FallOff" -nn "Light 1 Penumbra Angle" 
		-ct "HW_shader_parameter" -min 0 -max 1.5707962512969971 -at "float";
	addAttr -is true -ci true -h true -sn "light1AttenScale_Name" -ln "light1AttenScale_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light1AttenScale_Type" -ln "light1AttenScale_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light1AttenScale" -ln "light1AttenScale" 
		-nn "Light 1 Decay" -ct "HW_shader_parameter" -min 0 -max 99999 -smn 0 -smx 1 -at "float";
	addAttr -is true -ci true -h true -sn "light1ShadowOn_Name" -ln "light1ShadowOn_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light1ShadowOn_Type" -ln "light1ShadowOn_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light1ShadowOn" -ln "light1ShadowOn" -nn "Light 1 Casts Shadow" 
		-ct "HW_shader_parameter" -dv 1 -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "light2Enable_Name" -ln "light2Enable_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light2Enable_Type" -ln "light2Enable_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light2Enable" -ln "light2Enable" -nn "Enable Light 2" 
		-ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "light2Type_Name" -ln "light2Type_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "light2Type_Type" -ln "light2Type_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "light2Type" -ln "light2Type" -nn "Light 2 Type" 
		-ct "HW_shader_parameter" -dv 2 -min 0 -max 5 -smn 0 -smx 1 -en "None:Default:Spot:Point:Directional:Ambient" 
		-at "enum";
	addAttr -is true -ci true -h true -sn "light2Pos_Name" -ln "light2Pos_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "light2Pos_Type" -ln "light2Pos_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "light2Pos" -ln "light2Pos" -nn "Light 2 Position" 
		-ct "HW_shader_parameter" -at "matrix";
	addAttr -is true -ci true -h true -sn "light2Color_Name" -ln "light2Color_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light2Color_Type" -ln "light2Color_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -k true -sn "light2Color" -ln "light2Color" -nn "Light 2 Color" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "light2ColorR" -ln "light2ColorR" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "light2Color";
	addAttr -is true -ci true -sn "light2ColorG" -ln "light2ColorG" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "light2Color";
	addAttr -is true -ci true -sn "light2ColorB" -ln "light2ColorB" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "light2Color";
	addAttr -is true -ci true -h true -sn "light2Intensity_Name" -ln "light2Intensity_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light2Intensity_Type" -ln "light2Intensity_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light2Intensity" -ln "light2Intensity" -nn "Light 2 Intensity" 
		-ct "HW_shader_parameter" -dv 1 -min 0 -max 99999 -smn 0 -smx 1 -at "float";
	addAttr -is true -ci true -h true -sn "light2Dir_Name" -ln "light2Dir_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "light2Dir_Type" -ln "light2Dir_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "light2Dir" -ln "light2Dir" -nn "Light 2 Direction" 
		-ct "HW_shader_parameter" -at "matrix";
	addAttr -is true -ci true -h true -sn "light2ConeAngle_Name" -ln "light2ConeAngle_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light2ConeAngle_Type" -ln "light2ConeAngle_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light2ConeAngle" -ln "light2ConeAngle" -nn "Light 2 Cone Angle" 
		-ct "HW_shader_parameter" -dv 45 -min 0 -max 1.5707962512969971 -at "float";
	addAttr -is true -ci true -h true -sn "light2FallOff_Name" -ln "light2FallOff_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light2FallOff_Type" -ln "light2FallOff_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light2FallOff" -ln "light2FallOff" -nn "Light 2 Penumbra Angle" 
		-ct "HW_shader_parameter" -min 0 -max 1.5707962512969971 -at "float";
	addAttr -is true -ci true -h true -sn "light2AttenScale_Name" -ln "light2AttenScale_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light2AttenScale_Type" -ln "light2AttenScale_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "light2AttenScale" -ln "light2AttenScale" 
		-nn "Light 2 Decay" -ct "HW_shader_parameter" -min 0 -max 99999 -smn 0 -smx 1 -at "float";
	addAttr -is true -ci true -h true -sn "light2ShadowOn_Name" -ln "light2ShadowOn_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light2ShadowOn_Type" -ln "light2ShadowOn_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light2ShadowOn" -ln "light2ShadowOn" -nn "Light 2 Casts Shadow" 
		-ct "HW_shader_parameter" -dv 1 -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "rimFresnelMin_Name" -ln "rimFresnelMin_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "rimFresnelMin_Type" -ln "rimFresnelMin_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "rimFresnelMin" -ln "rimFresnelMin" -nn "Rim Light Min" 
		-ct "HW_shader_parameter" -dv 0.80000001192092896 -min 0 -max 1 -at "float";
	addAttr -is true -ci true -h true -sn "rimFresnelMax_Name" -ln "rimFresnelMax_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "rimFresnelMax_Type" -ln "rimFresnelMax_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "rimFresnelMax" -ln "rimFresnelMax" -nn "Rim Light Max" 
		-ct "HW_shader_parameter" -dv 1 -min 0 -max 1 -at "float";
	addAttr -is true -ci true -h true -sn "rimBrightness_Name" -ln "rimBrightness_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "rimBrightness_Type" -ln "rimBrightness_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "rimBrightness" -ln "rimBrightness" -nn "Rim Light Brightness" 
		-ct "HW_shader_parameter" -min 0 -max 99999 -smx 10 -at "float";
	addAttr -is true -ci true -h true -sn "UseEmissiveTexture_Name" -ln "UseEmissiveTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseEmissiveTexture_Type" -ln "UseEmissiveTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "UseEmissiveTexture" -ln "UseEmissiveTexture" 
		-nn "Emissive Map" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "EmissiveTexture_Name" -ln "EmissiveTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "EmissiveTexture_Type" -ln "EmissiveTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -sn "EmissiveTexture" -ln "EmissiveTexture" -nn "Emissive Map" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "EmissiveTextureR" -ln "EmissiveTextureR" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "EmissiveTexture";
	addAttr -is true -ci true -sn "EmissiveTextureG" -ln "EmissiveTextureG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "EmissiveTexture";
	addAttr -is true -ci true -sn "EmissiveTextureB" -ln "EmissiveTextureB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "EmissiveTexture";
	addAttr -is true -ci true -h true -sn "EmissiveIntensity_Name" -ln "EmissiveIntensity_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "EmissiveIntensity_Type" -ln "EmissiveIntensity_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "EmissiveIntensity" -ln "EmissiveIntensity" 
		-nn "Emissive Intensity" -ct "HW_shader_parameter" -dv 1 -min 0 -max 99999 -smn 0 
		-smx 1 -at "float";
	addAttr -is true -ci true -h true -sn "AmbientSkyColor_Name" -ln "AmbientSkyColor_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "AmbientSkyColor_Type" -ln "AmbientSkyColor_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -k true -sn "AmbientSkyColor" -ln "AmbientSkyColor" 
		-nn "Ambient Sky Color" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "AmbientSkyColorR" -ln "AmbientSkyColorR" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "AmbientSkyColor";
	addAttr -is true -ci true -sn "AmbientSkyColorG" -ln "AmbientSkyColorG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "AmbientSkyColor";
	addAttr -is true -ci true -sn "AmbientSkyColorB" -ln "AmbientSkyColorB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "AmbientSkyColor";
	addAttr -is true -ci true -h true -sn "AmbientGroundColor_Name" -ln "AmbientGroundColor_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "AmbientGroundColor_Type" -ln "AmbientGroundColor_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -k true -sn "AmbientGroundColor" -ln "AmbientGroundColor" 
		-nn "Ambient Ground Color" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "AmbientGroundColorR" -ln "AmbientGroundColorR" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "AmbientGroundColor";
	addAttr -is true -ci true -sn "AmbientGroundColorG" -ln "AmbientGroundColorG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "AmbientGroundColor";
	addAttr -is true -ci true -sn "AmbientGroundColorB" -ln "AmbientGroundColorB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "AmbientGroundColor";
	addAttr -is true -ci true -h true -sn "AmbientOcclusionTexture_Name" -ln "AmbientOcclusionTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "AmbientOcclusionTexture_Type" -ln "AmbientOcclusionTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "AmbientOcclusionTexture" -ln "AmbientOcclusionTexture" 
		-nn "Ambient Occlusion Map" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "AmbientOcclusionTextureR" -ln "AmbientOcclusionTextureR" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "AmbientOcclusionTexture";
	addAttr -is true -ci true -sn "AmbientOcclusionTextureG" -ln "AmbientOcclusionTextureG" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "AmbientOcclusionTexture";
	addAttr -is true -ci true -sn "AmbientOcclusionTextureB" -ln "AmbientOcclusionTextureB" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "AmbientOcclusionTexture";
	addAttr -is true -ci true -h true -sn "UseAmbientOcclusionTexture_Name" -ln "UseAmbientOcclusionTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseAmbientOcclusionTexture_Type" -ln "UseAmbientOcclusionTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "UseAmbientOcclusionTexture" -ln "UseAmbientOcclusionTexture" 
		-nn "Ambient Occlusion Map" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "DiffuseModel_Name" -ln "DiffuseModel_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseModel_Type" -ln "DiffuseModel_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseModel" -ln "DiffuseModel" -nn "Diffuse Model" 
		-ct "HW_shader_parameter" -min 0 -max 2 -smn 0 -smx 1 -en "Blended Normal (Skin)" 
		-at "enum";
	addAttr -is true -ci true -h true -sn "UseDiffuseTexture_Name" -ln "UseDiffuseTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseDiffuseTexture_Type" -ln "UseDiffuseTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "UseDiffuseTexture" -ln "UseDiffuseTexture" 
		-nn "Diffuse Map" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "UseDiffuseTextureAlpha_Name" -ln "UseDiffuseTextureAlpha_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseDiffuseTextureAlpha_Type" -ln "UseDiffuseTextureAlpha_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseDiffuseTextureAlpha" -ln "UseDiffuseTextureAlpha" 
		-nn "Diffuse Map Alpha" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "DiffuseTexture_Name" -ln "DiffuseTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseTexture_Type" -ln "DiffuseTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -sn "DiffuseTexture" -ln "DiffuseTexture" -nn "Diffuse Map" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "DiffuseTextureR" -ln "DiffuseTextureR" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "DiffuseTexture";
	addAttr -is true -ci true -sn "DiffuseTextureG" -ln "DiffuseTextureG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "DiffuseTexture";
	addAttr -is true -ci true -sn "DiffuseTextureB" -ln "DiffuseTextureB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "DiffuseTexture";
	addAttr -is true -ci true -h true -sn "DiffuseColor_Name" -ln "DiffuseColor_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseColor_Type" -ln "DiffuseColor_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -k true -sn "DiffuseColor" -ln "DiffuseColor" -nn "Diffuse Color" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "DiffuseColorR" -ln "DiffuseColorR" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "DiffuseColor";
	addAttr -is true -ci true -sn "DiffuseColorG" -ln "DiffuseColorG" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "DiffuseColor";
	addAttr -is true -ci true -sn "DiffuseColorB" -ln "DiffuseColorB" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "DiffuseColor";
	addAttr -is true -ci true -h true -sn "Opacity_Name" -ln "Opacity_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Opacity_Type" -ln "Opacity_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Opacity" -ln "Opacity" -nn "Opacity" -ct "HW_shader_parameter" 
		-dv 1 -min 0 -max 1 -at "float";
	addAttr -is true -ci true -h true -sn "UseOpacityMaskTexture_Name" -ln "UseOpacityMaskTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseOpacityMaskTexture_Type" -ln "UseOpacityMaskTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseOpacityMaskTexture" -ln "UseOpacityMaskTexture" 
		-nn "Opacity Mask" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "OpacityMaskTexture_Name" -ln "OpacityMaskTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "OpacityMaskTexture_Type" -ln "OpacityMaskTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "OpacityMaskTexture" -ln "OpacityMaskTexture" 
		-nn "Opacity Mask" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "OpacityMaskTextureR" -ln "OpacityMaskTextureR" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "OpacityMaskTexture";
	addAttr -is true -ci true -sn "OpacityMaskTextureG" -ln "OpacityMaskTextureG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "OpacityMaskTexture";
	addAttr -is true -ci true -sn "OpacityMaskTextureB" -ln "OpacityMaskTextureB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "OpacityMaskTexture";
	addAttr -is true -ci true -h true -sn "OpacityMaskBias_Name" -ln "OpacityMaskBias_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "OpacityMaskBias_Type" -ln "OpacityMaskBias_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "OpacityMaskBias" -ln "OpacityMaskBias" -nn "Opacity Mask Bias" 
		-ct "HW_shader_parameter" -dv 0.10000000149011612 -min 0 -max 1 -at "float";
	addAttr -is true -ci true -h true -sn "OpacityFresnelMin_Name" -ln "OpacityFresnelMin_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "OpacityFresnelMin_Type" -ln "OpacityFresnelMin_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "OpacityFresnelMin" -ln "OpacityFresnelMin" 
		-nn "Opacity Fresnel Min" -ct "HW_shader_parameter" -min 0 -max 1 -at "float";
	addAttr -is true -ci true -h true -sn "OpacityFresnelMax_Name" -ln "OpacityFresnelMax_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "OpacityFresnelMax_Type" -ln "OpacityFresnelMax_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "OpacityFresnelMax" -ln "OpacityFresnelMax" 
		-nn "Opacity Fresnel Max" -ct "HW_shader_parameter" -min 0 -max 1 -at "float";
	addAttr -is true -ci true -h true -sn "UseLightmapTexture_Name" -ln "UseLightmapTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseLightmapTexture_Type" -ln "UseLightmapTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseLightmapTexture" -ln "UseLightmapTexture" 
		-nn "Lightmap Map" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "LightmapTexture_Name" -ln "LightmapTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "LightmapTexture_Type" -ln "LightmapTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "LightmapTexture" -ln "LightmapTexture" 
		-nn "Lightmap Map" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "LightmapTextureR" -ln "LightmapTextureR" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "LightmapTexture";
	addAttr -is true -ci true -sn "LightmapTextureG" -ln "LightmapTextureG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "LightmapTexture";
	addAttr -is true -ci true -sn "LightmapTextureB" -ln "LightmapTextureB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "LightmapTexture";
	addAttr -is true -ci true -h true -sn "SpecularModel_Name" -ln "SpecularModel_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "SpecularModel_Type" -ln "SpecularModel_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "SpecularModel" -ln "SpecularModel" -nn "Specular Model" 
		-ct "HW_shader_parameter" -min 0 -max 2 -smn 0 -smx 1 -en "Blinn:Kelemen-Szirmaykalos (Skin):Anisotropic (Brushed Metal/Hair)" 
		-at "enum";
	addAttr -is true -ci true -h true -sn "UseSpecularTexture_Name" -ln "UseSpecularTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseSpecularTexture_Type" -ln "UseSpecularTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "UseSpecularTexture" -ln "UseSpecularTexture" 
		-nn "Specular Map" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "SpecularTexture_Name" -ln "SpecularTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "SpecularTexture_Type" -ln "SpecularTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -sn "SpecularTexture" -ln "SpecularTexture" -nn "Specular Map" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "SpecularTextureR" -ln "SpecularTextureR" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "SpecularTexture";
	addAttr -is true -ci true -sn "SpecularTextureG" -ln "SpecularTextureG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "SpecularTexture";
	addAttr -is true -ci true -sn "SpecularTextureB" -ln "SpecularTextureB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "SpecularTexture";
	addAttr -is true -ci true -h true -sn "SpecularColor_Name" -ln "SpecularColor_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "SpecularColor_Type" -ln "SpecularColor_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -k true -sn "SpecularColor" -ln "SpecularColor" -nn "Specular Color" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "SpecularColorR" -ln "SpecularColorR" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "SpecularColor";
	addAttr -is true -ci true -sn "SpecularColorG" -ln "SpecularColorG" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "SpecularColor";
	addAttr -is true -ci true -sn "SpecularColorB" -ln "SpecularColorB" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "SpecularColor";
	addAttr -is true -ci true -h true -sn "SpecPower_Name" -ln "SpecPower_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "SpecPower_Type" -ln "SpecPower_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "SpecPower" -ln "SpecPower" -nn "Specular Power" 
		-ct "HW_shader_parameter" -dv 20 -min 1 -max 99999 -smx 100 -at "float";
	addAttr -is true -ci true -h true -sn "UseAnisotropicDirectionMap_Name" -ln "UseAnisotropicDirectionMap_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseAnisotropicDirectionMap_Type" -ln "UseAnisotropicDirectionMap_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseAnisotropicDirectionMap" -ln "UseAnisotropicDirectionMap" 
		-nn "Anisotropic Direction Map" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "AnisotropicDirectionType_Name" -ln "AnisotropicDirectionType_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "AnisotropicDirectionType_Type" -ln "AnisotropicDirectionType_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "AnisotropicDirectionType" -ln "AnisotropicDirectionType" 
		-nn "Anisotropic Direction Type" -ct "HW_shader_parameter" -min 0 -max 0 -smn 0 -smx 
		1 -en "Tangent space (Comb/Flow map)" -at "enum";
	addAttr -is true -ci true -h true -sn "AnisotropicTexture_Name" -ln "AnisotropicTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "AnisotropicTexture_Type" -ln "AnisotropicTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "AnisotropicTexture" -ln "AnisotropicTexture" 
		-nn "Anisotropic Direction Map" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "AnisotropicTextureR" -ln "AnisotropicTextureR" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "AnisotropicTexture";
	addAttr -is true -ci true -sn "AnisotropicTextureG" -ln "AnisotropicTextureG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "AnisotropicTexture";
	addAttr -is true -ci true -sn "AnisotropicTextureB" -ln "AnisotropicTextureB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "AnisotropicTexture";
	addAttr -is true -ci true -h true -sn "AnisotropicRoughness1_Name" -ln "AnisotropicRoughness1_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "AnisotropicRoughness1_Type" -ln "AnisotropicRoughness1_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "AnisotropicRoughness1" -ln "AnisotropicRoughness1" 
		-nn "Anisotropic Roughness" -ct "HW_shader_parameter" -dv 0.20000000298023224 -min 
		-99999 -max 99999 -smn -1 -smx 1 -at "float";
	addAttr -is true -ci true -h true -sn "UseAnisotropicMapAlphaMask_Name" -ln "UseAnisotropicMapAlphaMask_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseAnisotropicMapAlphaMask_Type" -ln "UseAnisotropicMapAlphaMask_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseAnisotropicMapAlphaMask" -ln "UseAnisotropicMapAlphaMask" 
		-nn "Mix Blinn-Anisotropic by Direction Alpha" -ct "HW_shader_parameter" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -sn "UseNormalTexture_Name" -ln "UseNormalTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseNormalTexture_Type" -ln "UseNormalTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "UseNormalTexture" -ln "UseNormalTexture" 
		-nn "Normal Map" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "NormalTexture_Name" -ln "NormalTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "NormalTexture_Type" -ln "NormalTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -sn "NormalTexture" -ln "NormalTexture" -nn "Normal Map" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "NormalTextureR" -ln "NormalTextureR" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "NormalTexture";
	addAttr -is true -ci true -sn "NormalTextureG" -ln "NormalTextureG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "NormalTexture";
	addAttr -is true -ci true -sn "NormalTextureB" -ln "NormalTextureB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "NormalTexture";
	addAttr -is true -ci true -h true -sn "NormalHeight_Name" -ln "NormalHeight_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "NormalHeight_Type" -ln "NormalHeight_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "NormalHeight" -ln "NormalHeight" -nn "Normal Height" 
		-ct "HW_shader_parameter" -dv 1 -min 0 -max 99999 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "SupportNonUniformScale_Name" -ln "SupportNonUniformScale_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "SupportNonUniformScale_Type" -ln "SupportNonUniformScale_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "SupportNonUniformScale" -ln "SupportNonUniformScale" 
		-nn "Support Non-Uniform Scale" -ct "HW_shader_parameter" -dv 1 -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "NormalCoordsysX_Name" -ln "NormalCoordsysX_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "NormalCoordsysX_Type" -ln "NormalCoordsysX_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "NormalCoordsysX" -ln "NormalCoordsysX" -nn "Normal X (Red)" 
		-ct "HW_shader_parameter" -min 0 -max 1 -smn 0 -smx 1 -en "Positive:Negative" -at "enum";
	addAttr -is true -ci true -h true -sn "NormalCoordsysY_Name" -ln "NormalCoordsysY_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "NormalCoordsysY_Type" -ln "NormalCoordsysY_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "NormalCoordsysY" -ln "NormalCoordsysY" -nn "Normal Y (Green)" 
		-ct "HW_shader_parameter" -min 0 -max 1 -smn 0 -smx 1 -en "Positive:Negative" -at "enum";
	addAttr -is true -ci true -h true -sn "UseReflectionMap_Name" -ln "UseReflectionMap_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseReflectionMap_Type" -ln "UseReflectionMap_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "UseReflectionMap" -ln "UseReflectionMap" 
		-nn "Reflection Map" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "ReflectionType_Name" -ln "ReflectionType_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ReflectionType_Type" -ln "ReflectionType_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "ReflectionType" -ln "ReflectionType" -nn "Reflection Type" 
		-ct "HW_shader_parameter" -min 0 -max 4 -smn 0 -smx 1 -en "Cube:2D Spherical:2D LatLong:Cube & 2D Spherical:Cube & 2D LatLong" 
		-at "enum";
	addAttr -is true -ci true -h true -sn "ReflectionTextureCube_Name" -ln "ReflectionTextureCube_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ReflectionTextureCube_Type" -ln "ReflectionTextureCube_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -sn "ReflectionTextureCube" -ln "ReflectionTextureCube" 
		-nn "Reflection CubeMap" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "ReflectionTextureCubeR" -ln "ReflectionTextureCubeR" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "ReflectionTextureCube";
	addAttr -is true -ci true -sn "ReflectionTextureCubeG" -ln "ReflectionTextureCubeG" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "ReflectionTextureCube";
	addAttr -is true -ci true -sn "ReflectionTextureCubeB" -ln "ReflectionTextureCubeB" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "ReflectionTextureCube";
	addAttr -is true -ci true -h true -sn "ReflectionTexture2D_Name" -ln "ReflectionTexture2D_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ReflectionTexture2D_Type" -ln "ReflectionTexture2D_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -sn "ReflectionTexture2D" -ln "ReflectionTexture2D" 
		-nn "Reflection 2D Map" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "ReflectionTexture2DR" -ln "ReflectionTexture2DR" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "ReflectionTexture2D";
	addAttr -is true -ci true -sn "ReflectionTexture2DG" -ln "ReflectionTexture2DG" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "ReflectionTexture2D";
	addAttr -is true -ci true -sn "ReflectionTexture2DB" -ln "ReflectionTexture2DB" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "ReflectionTexture2D";
	addAttr -is true -ci true -h true -sn "ReflectionIntensity_Name" -ln "ReflectionIntensity_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ReflectionIntensity_Type" -ln "ReflectionIntensity_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "ReflectionIntensity" -ln "ReflectionIntensity" 
		-nn "Reflection Intensity" -ct "HW_shader_parameter" -dv 0.20000000298023224 -min 
		0 -max 99999 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "ReflectionBlur_Name" -ln "ReflectionBlur_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ReflectionBlur_Type" -ln "ReflectionBlur_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "ReflectionBlur" -ln "ReflectionBlur" -nn "Reflection Blur" 
		-ct "HW_shader_parameter" -min 0 -max 99999 -smx 10 -at "float";
	addAttr -is true -ci true -h true -sn "ReflectionRotation_Name" -ln "ReflectionRotation_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ReflectionRotation_Type" -ln "ReflectionRotation_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "ReflectionRotation" -ln "ReflectionRotation" 
		-nn "Reflection Rotation" -ct "HW_shader_parameter" -min 0 -max 99999 -smn 0 -smx 
		360 -at "float";
	addAttr -is true -ci true -h true -sn "ReflectionPinching_Name" -ln "ReflectionPinching_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ReflectionPinching_Type" -ln "ReflectionPinching_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "ReflectionPinching" -ln "ReflectionPinching" 
		-nn "Reflection Spherical Pinch" -ct "HW_shader_parameter" -dv 1.1000000238418579 
		-min 0 -max 99999 -smn 1 -smx 1.5 -at "float";
	addAttr -is true -ci true -h true -sn "ReflectionFresnelMin_Name" -ln "ReflectionFresnelMin_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ReflectionFresnelMin_Type" -ln "ReflectionFresnelMin_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "ReflectionFresnelMin" -ln "ReflectionFresnelMin" 
		-nn "Reflection Fresnel Min" -ct "HW_shader_parameter" -min 0 -max 1 -at "float";
	addAttr -is true -ci true -h true -sn "ReflectionFresnelMax_Name" -ln "ReflectionFresnelMax_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ReflectionFresnelMax_Type" -ln "ReflectionFresnelMax_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "ReflectionFresnelMax" -ln "ReflectionFresnelMax" 
		-nn "Reflection Fresnel Max" -ct "HW_shader_parameter" -min 0 -max 1 -at "float";
	addAttr -is true -ci true -h true -sn "UseReflectionMask_Name" -ln "UseReflectionMask_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseReflectionMask_Type" -ln "UseReflectionMask_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "UseReflectionMask" -ln "UseReflectionMask" 
		-nn "Reflection Mask" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "ReflectionMask_Name" -ln "ReflectionMask_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ReflectionMask_Type" -ln "ReflectionMask_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -sn "ReflectionMask" -ln "ReflectionMask" -nn "Reflection Mask" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "ReflectionMaskR" -ln "ReflectionMaskR" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "ReflectionMask";
	addAttr -is true -ci true -sn "ReflectionMaskG" -ln "ReflectionMaskG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "ReflectionMask";
	addAttr -is true -ci true -sn "ReflectionMaskB" -ln "ReflectionMaskB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "ReflectionMask";
	addAttr -is true -ci true -h true -sn "UseSpecAlphaForReflectionBlur_Name" -ln "UseSpecAlphaForReflectionBlur_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseSpecAlphaForReflectionBlur_Type" -ln "UseSpecAlphaForReflectionBlur_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "UseSpecAlphaForReflectionBlur" -ln "UseSpecAlphaForReflectionBlur" 
		-nn "Spec Alpha For Reflection Blur" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "UseSpecColorToTintReflection_Name" -ln "UseSpecColorToTintReflection_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseSpecColorToTintReflection_Type" -ln "UseSpecColorToTintReflection_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "UseSpecColorToTintReflection" -ln "UseSpecColorToTintReflection" 
		-nn "Spec Color to Tint Reflection" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "ReflectionAffectOpacity_Name" -ln "ReflectionAffectOpacity_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ReflectionAffectOpacity_Type" -ln "ReflectionAffectOpacity_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "ReflectionAffectOpacity" -ln "ReflectionAffectOpacity" 
		-nn "Reflections Affect Opacity" -ct "HW_shader_parameter" -dv 1 -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "DisplacementModel_Name" -ln "DisplacementModel_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DisplacementModel_Type" -ln "DisplacementModel_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DisplacementModel" -ln "DisplacementModel" 
		-nn "Displacement Model" -ct "HW_shader_parameter" -min 0 -max 1 -smn 0 -smx 1 -en 
		"Grayscale:Tangent Vector" -at "enum";
	addAttr -is true -ci true -h true -sn "UseDisplacementMap_Name" -ln "UseDisplacementMap_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseDisplacementMap_Type" -ln "UseDisplacementMap_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseDisplacementMap" -ln "UseDisplacementMap" 
		-nn "Displacement Map" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "DisplacementTexture_Name" -ln "DisplacementTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DisplacementTexture_Type" -ln "DisplacementTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "DisplacementTexture" -ln "DisplacementTexture" 
		-nn "Displacement Map" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "DisplacementTextureR" -ln "DisplacementTextureR" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "DisplacementTexture";
	addAttr -is true -ci true -sn "DisplacementTextureG" -ln "DisplacementTextureG" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "DisplacementTexture";
	addAttr -is true -ci true -sn "DisplacementTextureB" -ln "DisplacementTextureB" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "DisplacementTexture";
	addAttr -is true -ci true -h true -sn "VectorDisplacementCoordSys_Name" -ln "VectorDisplacementCoordSys_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "VectorDisplacementCoordSys_Type" -ln "VectorDisplacementCoordSys_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "VectorDisplacementCoordSys" -ln "VectorDisplacementCoordSys" 
		-nn "Displacement Coordsys" -ct "HW_shader_parameter" -min 0 -max 1 -smn 0 -smx 1 
		-en "Mudbox (XZY):Maya (XYZ)" -at "enum";
	addAttr -is true -ci true -h true -sn "DisplacementHeight_Name" -ln "DisplacementHeight_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DisplacementHeight_Type" -ln "DisplacementHeight_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DisplacementHeight" -ln "DisplacementHeight" 
		-nn "Displacement Height" -ct "HW_shader_parameter" -dv 0.5 -min -99999 -max 99999 
		-smn 0 -smx 10 -at "float";
	addAttr -is true -ci true -h true -sn "DisplacementOffset_Name" -ln "DisplacementOffset_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DisplacementOffset_Type" -ln "DisplacementOffset_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DisplacementOffset" -ln "DisplacementOffset" 
		-nn "Displacement Offset" -ct "HW_shader_parameter" -dv 0.5 -min -99999 -max 99999 
		-smn -1 -smx 1 -at "float";
	addAttr -is true -ci true -h true -sn "DisplacementClippingBias_Name" -ln "DisplacementClippingBias_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DisplacementClippingBias_Type" -ln "DisplacementClippingBias_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DisplacementClippingBias" -ln "DisplacementClippingBias" 
		-nn "Displacement Clipping Bias" -ct "HW_shader_parameter" -dv 5 -min -99999 -max 
		99999 -smn 0 -smx 99 -at "float";
	addAttr -is true -ci true -h true -sn "BBoxExtraScale_Name" -ln "BBoxExtraScale_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "BBoxExtraScale_Type" -ln "BBoxExtraScale_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "BBoxExtraScale" -ln "BBoxExtraScale" -nn "Bounding Box Extra Scale" 
		-ct "HW_shader_parameter" -dv 1 -min 1 -max 99999 -smx 10 -at "float";
	addAttr -is true -ci true -h true -sn "TessellationRange_Name" -ln "TessellationRange_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "TessellationRange_Type" -ln "TessellationRange_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "TessellationRange" -ln "TessellationRange" 
		-nn "Tessellation Range" -ct "HW_shader_parameter" -min 0 -max 99999 -smx 999 -at "float";
	addAttr -is true -ci true -h true -sn "TessellationMin_Name" -ln "TessellationMin_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "TessellationMin_Type" -ln "TessellationMin_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "TessellationMin" -ln "TessellationMin" -nn "Tessellation Minimum" 
		-ct "HW_shader_parameter" -dv 3 -min 1 -max 99999 -smx 10 -at "float";
	addAttr -is true -ci true -h true -sn "FlatTessellation_Name" -ln "FlatTessellation_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "FlatTessellation_Type" -ln "FlatTessellation_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "FlatTessellation" -ln "FlatTessellation" 
		-nn "Flat Tessellation" -ct "HW_shader_parameter" -min 0 -max 1 -at "float";
	addAttr -is true -ci true -h true -sn "UseTranslucency_Name" -ln "UseTranslucency_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseTranslucency_Type" -ln "UseTranslucency_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseTranslucency" -ln "UseTranslucency" -nn "Translucency" 
		-ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "UseThicknessTexture_Name" -ln "UseThicknessTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseThicknessTexture_Type" -ln "UseThicknessTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseThicknessTexture" -ln "UseThicknessTexture" 
		-nn "Thickness Mask" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "TranslucencyThicknessMask_Name" -ln "TranslucencyThicknessMask_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "TranslucencyThicknessMask_Type" -ln "TranslucencyThicknessMask_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "TranslucencyThicknessMask" -ln "TranslucencyThicknessMask" 
		-nn "Thickness Mask" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "TranslucencyThicknessMaskR" -ln "TranslucencyThicknessMaskR" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "TranslucencyThicknessMask";
	addAttr -is true -ci true -sn "TranslucencyThicknessMaskG" -ln "TranslucencyThicknessMaskG" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "TranslucencyThicknessMask";
	addAttr -is true -ci true -sn "TranslucencyThicknessMaskB" -ln "TranslucencyThicknessMaskB" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "TranslucencyThicknessMask";
	addAttr -is true -ci true -h true -sn "translucentDistortion_Name" -ln "translucentDistortion_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "translucentDistortion_Type" -ln "translucentDistortion_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "translucentDistortion" -ln "translucentDistortion" 
		-nn "Light Translucent Distortion" -ct "HW_shader_parameter" -dv 0.20000000298023224 
		-min 0 -max 99999 -smx 10 -at "float";
	addAttr -is true -ci true -h true -sn "translucentPower_Name" -ln "translucentPower_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "translucentPower_Type" -ln "translucentPower_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "translucentPower" -ln "translucentPower" 
		-nn "Light Translucent Power" -ct "HW_shader_parameter" -dv 3 -min 0 -max 99999 -smx 
		20 -at "float";
	addAttr -is true -ci true -h true -sn "translucentScale_Name" -ln "translucentScale_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "translucentScale_Type" -ln "translucentScale_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "translucentScale" -ln "translucentScale" 
		-nn "Light Translucent Scale" -ct "HW_shader_parameter" -dv 1 -min 0 -max 99999 -smx 
		1 -at "float";
	addAttr -is true -ci true -h true -sn "translucentMin_Name" -ln "translucentMin_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "translucentMin_Type" -ln "translucentMin_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "translucentMin" -ln "translucentMin" -nn "Translucent Minimum" 
		-ct "HW_shader_parameter" -min 0 -max 99999 -smx 1 -at "float";
	addAttr -is true -ci true -h true -sn "SkinRampOuterColor_Name" -ln "SkinRampOuterColor_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "SkinRampOuterColor_Type" -ln "SkinRampOuterColor_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "SkinRampOuterColor" -ln "SkinRampOuterColor" 
		-nn "Outer Translucent Color" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "SkinRampOuterColorR" -ln "SkinRampOuterColorR" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "SkinRampOuterColor";
	addAttr -is true -ci true -sn "SkinRampOuterColorG" -ln "SkinRampOuterColorG" -ct "HW_shader_parameter" 
		-dv 0.63999998569488525 -smn 0 -smx 1 -at "float" -p "SkinRampOuterColor";
	addAttr -is true -ci true -sn "SkinRampOuterColorB" -ln "SkinRampOuterColorB" -ct "HW_shader_parameter" 
		-dv 0.25 -smn 0 -smx 1 -at "float" -p "SkinRampOuterColor";
	addAttr -is true -ci true -h true -sn "SkinRampMediumColor_Name" -ln "SkinRampMediumColor_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "SkinRampMediumColor_Type" -ln "SkinRampMediumColor_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "SkinRampMediumColor" -ln "SkinRampMediumColor" 
		-nn "Medium Translucent Color" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "SkinRampMediumColorR" -ln "SkinRampMediumColorR" 
		-ct "HW_shader_parameter" -dv 1 -smn 0 -smx 1 -at "float" -p "SkinRampMediumColor";
	addAttr -is true -ci true -sn "SkinRampMediumColorG" -ln "SkinRampMediumColorG" 
		-ct "HW_shader_parameter" -dv 0.20999999344348907 -smn 0 -smx 1 -at "float" -p "SkinRampMediumColor";
	addAttr -is true -ci true -sn "SkinRampMediumColorB" -ln "SkinRampMediumColorB" 
		-ct "HW_shader_parameter" -dv 0.14000000059604645 -smn 0 -smx 1 -at "float" -p "SkinRampMediumColor";
	addAttr -is true -ci true -h true -sn "SkinRampInnerColor_Name" -ln "SkinRampInnerColor_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "SkinRampInnerColor_Type" -ln "SkinRampInnerColor_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "SkinRampInnerColor" -ln "SkinRampInnerColor" 
		-nn "Inner Translucent Color" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "SkinRampInnerColorR" -ln "SkinRampInnerColorR" -ct "HW_shader_parameter" 
		-dv 0.25 -smn 0 -smx 1 -at "float" -p "SkinRampInnerColor";
	addAttr -is true -ci true -sn "SkinRampInnerColorG" -ln "SkinRampInnerColorG" -ct "HW_shader_parameter" 
		-dv 0.05000000074505806 -smn 0 -smx 1 -at "float" -p "SkinRampInnerColor";
	addAttr -is true -ci true -sn "SkinRampInnerColorB" -ln "SkinRampInnerColorB" -ct "HW_shader_parameter" 
		-dv 0.019999999552965164 -smn 0 -smx 1 -at "float" -p "SkinRampInnerColor";
	addAttr -is true -ci true -h true -sn "UseBlendedNormalTexture_Name" -ln "UseBlendedNormalTexture_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseBlendedNormalTexture_Type" -ln "UseBlendedNormalTexture_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "UseBlendedNormalTexture" -ln "UseBlendedNormalTexture" 
		-nn "Blended Normal Mask" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "BlendedNormalMask_Name" -ln "BlendedNormalMask_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "BlendedNormalMask_Type" -ln "BlendedNormalMask_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -sn "BlendedNormalMask" -ln "BlendedNormalMask" -nn "Blended Normal Mask" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "BlendedNormalMaskR" -ln "BlendedNormalMaskR" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "BlendedNormalMask";
	addAttr -is true -ci true -sn "BlendedNormalMaskG" -ln "BlendedNormalMaskG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "BlendedNormalMask";
	addAttr -is true -ci true -sn "BlendedNormalMaskB" -ln "BlendedNormalMaskB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "BlendedNormalMask";
	addAttr -is true -ci true -h true -sn "blendNorm_Name" -ln "blendNorm_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "blendNorm_Type" -ln "blendNorm_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "blendNorm" -ln "blendNorm" -nn "Blended Normal" 
		-ct "HW_shader_parameter" -dv 0.15000000596046448 -min 0 -max 99999 -smx 1 -at "float";
	addAttr -is true -ci true -h true -sn "UseDiffuseIBLMap_Name" -ln "UseDiffuseIBLMap_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseDiffuseIBLMap_Type" -ln "UseDiffuseIBLMap_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "UseDiffuseIBLMap" -ln "UseDiffuseIBLMap" 
		-nn "IBL Map" -ct "HW_shader_parameter" -min 0 -max 1 -at "bool";
	addAttr -is true -ci true -h true -sn "DiffuseIBLTextureCube_Name" -ln "DiffuseIBLTextureCube_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseIBLTextureCube_Type" -ln "DiffuseIBLTextureCube_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "DiffuseIBLTextureCube" -ln "DiffuseIBLTextureCube" 
		-nn "IBL Cube Map" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "DiffuseIBLTextureCubeR" -ln "DiffuseIBLTextureCubeR" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "DiffuseIBLTextureCube";
	addAttr -is true -ci true -sn "DiffuseIBLTextureCubeG" -ln "DiffuseIBLTextureCubeG" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "DiffuseIBLTextureCube";
	addAttr -is true -ci true -sn "DiffuseIBLTextureCubeB" -ln "DiffuseIBLTextureCubeB" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "DiffuseIBLTextureCube";
	addAttr -is true -ci true -h true -sn "DiffuseIBLTexture2D_Name" -ln "DiffuseIBLTexture2D_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseIBLTexture2D_Type" -ln "DiffuseIBLTexture2D_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "DiffuseIBLTexture2D" -ln "DiffuseIBLTexture2D" 
		-nn "IBL 2D Map" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "DiffuseIBLTexture2DR" -ln "DiffuseIBLTexture2DR" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "DiffuseIBLTexture2D";
	addAttr -is true -ci true -sn "DiffuseIBLTexture2DG" -ln "DiffuseIBLTexture2DG" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "DiffuseIBLTexture2D";
	addAttr -is true -ci true -sn "DiffuseIBLTexture2DB" -ln "DiffuseIBLTexture2DB" 
		-ct "HW_shader_parameter" -smn 0 -smx 1 -at "float" -p "DiffuseIBLTexture2D";
	addAttr -is true -ci true -h true -sn "DiffuseIBLType_Name" -ln "DiffuseIBLType_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseIBLType_Type" -ln "DiffuseIBLType_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseIBLType" -ln "DiffuseIBLType" -nn "IBL Type" 
		-ct "HW_shader_parameter" -min 0 -max 4 -smn 0 -smx 1 -en "Cube:2D Spherical:2D LatLong:Cube & 2D Spherical:Cube & 2D LatLong" 
		-at "enum";
	addAttr -is true -ci true -h true -sn "DiffuseIBLIntensity_Name" -ln "DiffuseIBLIntensity_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseIBLIntensity_Type" -ln "DiffuseIBLIntensity_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseIBLIntensity" -ln "DiffuseIBLIntensity" 
		-nn "IBL Intensity" -ct "HW_shader_parameter" -dv 0.5 -min 0 -max 99999 -smx 2 -at "float";
	addAttr -is true -ci true -h true -sn "DiffuseIBLBlur_Name" -ln "DiffuseIBLBlur_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseIBLBlur_Type" -ln "DiffuseIBLBlur_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseIBLBlur" -ln "DiffuseIBLBlur" -nn "IBL Blur" 
		-ct "HW_shader_parameter" -dv 5 -min 0 -max 99999 -smx 10 -at "float";
	addAttr -is true -ci true -h true -sn "DiffuseIBLRotation_Name" -ln "DiffuseIBLRotation_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseIBLRotation_Type" -ln "DiffuseIBLRotation_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseIBLRotation" -ln "DiffuseIBLRotation" 
		-nn "IBL Rotation" -ct "HW_shader_parameter" -min 0 -max 99999 -smn 0 -smx 360 -at "float";
	addAttr -is true -ci true -h true -sn "DiffuseIBLPinching_Name" -ln "DiffuseIBLPinching_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseIBLPinching_Type" -ln "DiffuseIBLPinching_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseIBLPinching" -ln "DiffuseIBLPinching" 
		-nn "IBL Spherical Pinch" -ct "HW_shader_parameter" -dv 1.1000000238418579 -min 0 
		-max 99999 -smn 1 -smx 1.5 -at "float";
	addAttr -is true -ci true -h true -sn "EmissiveTexcoord_Name" -ln "EmissiveTexcoord_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "EmissiveTexcoord_Type" -ln "EmissiveTexcoord_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "EmissiveTexcoord" -ln "EmissiveTexcoord" 
		-nn "Emissive Map" -ct "HW_shader_parameter" -min 0 -max 2 -smn 0 -smx 1 -en "TexCoord0:TexCoord1:TexCoord2" 
		-at "enum";
	addAttr -is true -ci true -h true -sn "DiffuseTexcoord_Name" -ln "DiffuseTexcoord_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DiffuseTexcoord_Type" -ln "DiffuseTexcoord_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "DiffuseTexcoord" -ln "DiffuseTexcoord" -nn "Diffuse Map" 
		-ct "HW_shader_parameter" -min 0 -max 2 -smn 0 -smx 1 -en "TexCoord0:TexCoord1:TexCoord2" 
		-at "enum";
	addAttr -is true -ci true -h true -sn "LightmapTexcoord_Name" -ln "LightmapTexcoord_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "LightmapTexcoord_Type" -ln "LightmapTexcoord_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "LightmapTexcoord" -ln "LightmapTexcoord" 
		-nn "Light Map" -ct "HW_shader_parameter" -dv 1 -min 0 -max 2 -smn 0 -smx 1 -en "TexCoord0:TexCoord1:TexCoord2" 
		-at "enum";
	addAttr -is true -ci true -h true -sn "AmbientOcclusionTexcoord_Name" -ln "AmbientOcclusionTexcoord_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "AmbientOcclusionTexcoord_Type" -ln "AmbientOcclusionTexcoord_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "AmbientOcclusionTexcoord" -ln "AmbientOcclusionTexcoord" 
		-nn "Ambient Occlusion Map" -ct "HW_shader_parameter" -dv 1 -min 0 -max 2 -smn 0 
		-smx 1 -en "TexCoord0:TexCoord1:TexCoord2" -at "enum";
	addAttr -is true -ci true -h true -sn "BlendedNormalMaskTexcoord_Name" -ln "BlendedNormalMaskTexcoord_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "BlendedNormalMaskTexcoord_Type" -ln "BlendedNormalMaskTexcoord_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "BlendedNormalMaskTexcoord" -ln "BlendedNormalMaskTexcoord" 
		-nn "Blended Normal Mask" -ct "HW_shader_parameter" -min 0 -max 2 -smn 0 -smx 1 -en 
		"TexCoord0:TexCoord1:TexCoord2" -at "enum";
	addAttr -is true -ci true -h true -sn "OpacityMaskTexcoord_Name" -ln "OpacityMaskTexcoord_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "OpacityMaskTexcoord_Type" -ln "OpacityMaskTexcoord_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "OpacityMaskTexcoord" -ln "OpacityMaskTexcoord" 
		-nn "Opacity Mask" -ct "HW_shader_parameter" -min 0 -max 2 -smn 0 -smx 1 -en "TexCoord0:TexCoord1:TexCoord2" 
		-at "enum";
	addAttr -is true -ci true -h true -sn "SpecularTexcoord_Name" -ln "SpecularTexcoord_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "SpecularTexcoord_Type" -ln "SpecularTexcoord_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "SpecularTexcoord" -ln "SpecularTexcoord" 
		-nn "Specular Map" -ct "HW_shader_parameter" -min 0 -max 2 -smn 0 -smx 1 -en "TexCoord0:TexCoord1:TexCoord2" 
		-at "enum";
	addAttr -is true -ci true -h true -sn "AnisotropicTexcoord_Name" -ln "AnisotropicTexcoord_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "AnisotropicTexcoord_Type" -ln "AnisotropicTexcoord_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "AnisotropicTexcoord" -ln "AnisotropicTexcoord" 
		-nn "Anisotropic Direction Map" -ct "HW_shader_parameter" -min 0 -max 2 -smn 0 -smx 
		1 -en "TexCoord0:TexCoord1:TexCoord2" -at "enum";
	addAttr -is true -ci true -h true -sn "NormalTexcoord_Name" -ln "NormalTexcoord_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "NormalTexcoord_Type" -ln "NormalTexcoord_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "NormalTexcoord" -ln "NormalTexcoord" -nn "Normal Map" 
		-ct "HW_shader_parameter" -min 0 -max 2 -smn 0 -smx 1 -en "TexCoord0:TexCoord1:TexCoord2" 
		-at "enum";
	addAttr -is true -ci true -h true -sn "ReflectionMaskTexcoord_Name" -ln "ReflectionMaskTexcoord_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ReflectionMaskTexcoord_Type" -ln "ReflectionMaskTexcoord_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ReflectionMaskTexcoord" -ln "ReflectionMaskTexcoord" 
		-nn "Reflection Mask" -ct "HW_shader_parameter" -min 0 -max 2 -smn 0 -smx 1 -en "TexCoord0:TexCoord1:TexCoord2" 
		-at "enum";
	addAttr -is true -ci true -h true -sn "DisplacementTexcoord_Name" -ln "DisplacementTexcoord_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DisplacementTexcoord_Type" -ln "DisplacementTexcoord_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "DisplacementTexcoord" -ln "DisplacementTexcoord" 
		-nn "Displacement Map" -ct "HW_shader_parameter" -min 0 -max 2 -smn 0 -smx 1 -en 
		"TexCoord0:TexCoord1:TexCoord2" -at "enum";
	addAttr -is true -ci true -h true -sn "ThicknessTexcoord_Name" -ln "ThicknessTexcoord_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ThicknessTexcoord_Type" -ln "ThicknessTexcoord_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ThicknessTexcoord" -ln "ThicknessTexcoord" 
		-nn "Translucency Mask" -ct "HW_shader_parameter" -min 0 -max 2 -smn 0 -smx 1 -en 
		"TexCoord0:TexCoord1:TexCoord2" -at "enum";
	addAttr -is true -ci true -h true -sn "light0ShadowMap_Name" -ln "light0ShadowMap_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light0ShadowMap_Type" -ln "light0ShadowMap_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "light0ShadowMap" -ln "light0ShadowMap" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "light0ShadowMapR" -ln "light0ShadowMapR" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "light0ShadowMap";
	addAttr -is true -ci true -sn "light0ShadowMapG" -ln "light0ShadowMapG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "light0ShadowMap";
	addAttr -is true -ci true -sn "light0ShadowMapB" -ln "light0ShadowMapB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "light0ShadowMap";
	addAttr -is true -ci true -h true -sn "light1ShadowMap_Name" -ln "light1ShadowMap_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light1ShadowMap_Type" -ln "light1ShadowMap_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "light1ShadowMap" -ln "light1ShadowMap" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "light1ShadowMapR" -ln "light1ShadowMapR" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "light1ShadowMap";
	addAttr -is true -ci true -sn "light1ShadowMapG" -ln "light1ShadowMapG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "light1ShadowMap";
	addAttr -is true -ci true -sn "light1ShadowMapB" -ln "light1ShadowMapB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "light1ShadowMap";
	addAttr -is true -ci true -h true -sn "light2ShadowMap_Name" -ln "light2ShadowMap_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "light2ShadowMap_Type" -ln "light2ShadowMap_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "light2ShadowMap" -ln "light2ShadowMap" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "light2ShadowMapR" -ln "light2ShadowMapR" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "light2ShadowMap";
	addAttr -is true -ci true -sn "light2ShadowMapG" -ln "light2ShadowMapG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "light2ShadowMap";
	addAttr -is true -ci true -sn "light2ShadowMapB" -ln "light2ShadowMapB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "light2ShadowMap";
	addAttr -ci true -sn "Position" -ln "Position" -at "compound" -nc 3;
	addAttr -is true -ci true -h true -sn "Position_Name" -ln "Position_Name" -ct "HW_shader_parameter" 
		-dt "string" -p "Position";
	addAttr -is true -ci true -h true -sn "Position_Source" -ln "Position_Source" -ct "HW_shader_parameter" 
		-dt "string" -p "Position";
	addAttr -is true -ci true -sn "Position_DefaultTexture" -ln "Position_DefaultTexture" 
		-ct "HW_shader_parameter" -dt "string" -p "Position";
	addAttr -ci true -sn "TexCoord0" -ln "TexCoord0" -at "compound" -nc 3;
	addAttr -is true -ci true -h true -sn "TexCoord0_Name" -ln "TexCoord0_Name" -ct "HW_shader_parameter" 
		-dt "string" -p "TexCoord0";
	addAttr -is true -ci true -h true -sn "TexCoord0_Source" -ln "TexCoord0_Source" 
		-ct "HW_shader_parameter" -dt "string" -p "TexCoord0";
	addAttr -is true -ci true -sn "TexCoord0_DefaultTexture" -ln "TexCoord0_DefaultTexture" 
		-ct "HW_shader_parameter" -dt "string" -p "TexCoord0";
	addAttr -ci true -sn "TexCoord1" -ln "TexCoord1" -at "compound" -nc 3;
	addAttr -is true -ci true -h true -sn "TexCoord1_Name" -ln "TexCoord1_Name" -ct "HW_shader_parameter" 
		-dt "string" -p "TexCoord1";
	addAttr -is true -ci true -h true -sn "TexCoord1_Source" -ln "TexCoord1_Source" 
		-ct "HW_shader_parameter" -dt "string" -p "TexCoord1";
	addAttr -is true -ci true -sn "TexCoord1_DefaultTexture" -ln "TexCoord1_DefaultTexture" 
		-ct "HW_shader_parameter" -dt "string" -p "TexCoord1";
	addAttr -ci true -sn "TexCoord2" -ln "TexCoord2" -at "compound" -nc 3;
	addAttr -is true -ci true -h true -sn "TexCoord2_Name" -ln "TexCoord2_Name" -ct "HW_shader_parameter" 
		-dt "string" -p "TexCoord2";
	addAttr -is true -ci true -h true -sn "TexCoord2_Source" -ln "TexCoord2_Source" 
		-ct "HW_shader_parameter" -dt "string" -p "TexCoord2";
	addAttr -is true -ci true -sn "TexCoord2_DefaultTexture" -ln "TexCoord2_DefaultTexture" 
		-ct "HW_shader_parameter" -dt "string" -p "TexCoord2";
	addAttr -ci true -sn "Normal" -ln "Normal" -at "compound" -nc 3;
	addAttr -is true -ci true -h true -sn "Normal_Name" -ln "Normal_Name" -ct "HW_shader_parameter" 
		-dt "string" -p "Normal";
	addAttr -is true -ci true -h true -sn "Normal_Source" -ln "Normal_Source" -ct "HW_shader_parameter" 
		-dt "string" -p "Normal";
	addAttr -is true -ci true -sn "Normal_DefaultTexture" -ln "Normal_DefaultTexture" 
		-ct "HW_shader_parameter" -dt "string" -p "Normal";
	addAttr -ci true -sn "Binormal0" -ln "Binormal0" -at "compound" -nc 3;
	addAttr -is true -ci true -h true -sn "Binormal0_Name" -ln "Binormal0_Name" -ct "HW_shader_parameter" 
		-dt "string" -p "Binormal0";
	addAttr -is true -ci true -h true -sn "Binormal0_Source" -ln "Binormal0_Source" 
		-ct "HW_shader_parameter" -dt "string" -p "Binormal0";
	addAttr -is true -ci true -sn "Binormal0_DefaultTexture" -ln "Binormal0_DefaultTexture" 
		-ct "HW_shader_parameter" -dt "string" -p "Binormal0";
	addAttr -ci true -sn "Tangent0" -ln "Tangent0" -at "compound" -nc 3;
	addAttr -is true -ci true -h true -sn "Tangent0_Name" -ln "Tangent0_Name" -ct "HW_shader_parameter" 
		-dt "string" -p "Tangent0";
	addAttr -is true -ci true -h true -sn "Tangent0_Source" -ln "Tangent0_Source" -ct "HW_shader_parameter" 
		-dt "string" -p "Tangent0";
	addAttr -is true -ci true -sn "Tangent0_DefaultTexture" -ln "Tangent0_DefaultTexture" 
		-ct "HW_shader_parameter" -dt "string" -p "Tangent0";
	addAttr -is true -ci true -h true -sn "ShadowColor_Name" -ln "ShadowColor_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ShadowColor_Type" -ln "ShadowColor_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -k true -sn "ShadowColor" -ln "ShadowColor" -nn "Shadow Color" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "ShadowColorR" -ln "ShadowColorR" -ct "HW_shader_parameter" 
		-dv 0.20000000298023224 -smn 0 -smx 1 -at "float" -p "ShadowColor";
	addAttr -is true -ci true -sn "ShadowColorG" -ln "ShadowColorG" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "ShadowColor";
	addAttr -is true -ci true -sn "ShadowColorB" -ln "ShadowColorB" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "ShadowColor";
	addAttr -is true -ci true -h true -sn "ShadowSpread_Name" -ln "ShadowSpread_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ShadowSpread_Type" -ln "ShadowSpread_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "ShadowSpread" -ln "ShadowSpread" -nn "Shadow Spread" 
		-ct "HW_shader_parameter" -dv 1 -min 9.9999997473787516e-06 -smx 10 -at "float";
	addAttr -is true -ci true -h true -sn "ShadowSamples_Name" -ln "ShadowSamples_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "ShadowSamples_Type" -ln "ShadowSamples_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -k true -sn "ShadowSamples" -ln "ShadowSamples" -nn "Shadow Samples" 
		-ct "HW_shader_parameter" -dv 60 -min 1 -smx 200 -at "float";
	addAttr -is true -ci true -h true -sn "SpecularColor2_Name" -ln "SpecularColor2_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "SpecularColor2_Type" -ln "SpecularColor2_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -k true -sn "SpecularColor2" -ln "SpecularColor2" 
		-nn "Specular Color 2" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "SpecularColor2R" -ln "SpecularColor2R" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "SpecularColor2";
	addAttr -is true -ci true -sn "SpecularColor2G" -ln "SpecularColor2G" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "SpecularColor2";
	addAttr -is true -ci true -sn "SpecularColor2B" -ln "SpecularColor2B" -ct "HW_shader_parameter" 
		-dv 1 -smn 0 -smx 1 -at "float" -p "SpecularColor2";
	addAttr -is true -ci true -h true -sn "SpecPower2_Name" -ln "SpecPower2_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "SpecPower2_Type" -ln "SpecPower2_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "SpecPower2" -ln "SpecPower2" -nn "Specular Power 2" 
		-ct "HW_shader_parameter" -dv 5 -min 1 -smx 100 -at "float";
	addAttr -is true -ci true -h true -sn "AnisotropicSpecularColor_Name" -ln "AnisotropicSpecularColor_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "AnisotropicSpecularColor_Type" -ln "AnisotropicSpecularColor_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -h true -sn "AnisotropicSpecularColor" -ln "AnisotropicSpecularColor" 
		-nn "Anisotropic Specular Color" -ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "AnisotropicSpecularColorR" -ln "AnisotropicSpecularColorR" 
		-ct "HW_shader_parameter" -dv 1 -smn 0 -smx 1 -at "float" -p "AnisotropicSpecularColor";
	addAttr -is true -ci true -sn "AnisotropicSpecularColorG" -ln "AnisotropicSpecularColorG" 
		-ct "HW_shader_parameter" -dv 1 -smn 0 -smx 1 -at "float" -p "AnisotropicSpecularColor";
	addAttr -is true -ci true -sn "AnisotropicSpecularColorB" -ln "AnisotropicSpecularColorB" 
		-ct "HW_shader_parameter" -dv 1 -smn 0 -smx 1 -at "float" -p "AnisotropicSpecularColor";
	addAttr -is true -ci true -h true -sn "CompExpTexture1_Name" -ln "CompExpTexture1_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "CompExpTexture1_Type" -ln "CompExpTexture1_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -sn "CompExpTexture1" -ln "CompExpTexture1" -nn "Wrinkle Normal" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "CompExpTexture1R" -ln "CompExpTexture1R" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "CompExpTexture1";
	addAttr -is true -ci true -sn "CompExpTexture1G" -ln "CompExpTexture1G" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "CompExpTexture1";
	addAttr -is true -ci true -sn "CompExpTexture1B" -ln "CompExpTexture1B" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "CompExpTexture1";
	addAttr -is true -ci true -h true -sn "CavityTexture1_Name" -ln "CavityTexture1_Name" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -h true -sn "CavityTexture1_Type" -ln "CavityTexture1_Type" 
		-ct "HW_shader_parameter" -dt "string";
	addAttr -is true -ci true -uac -sn "CavityTexture1" -ln "CavityTexture1" -nn "Wrinkle Color" 
		-ct "HW_shader_parameter" -at "float3" -nc 3;
	addAttr -is true -ci true -sn "CavityTexture1R" -ln "CavityTexture1R" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "CavityTexture1";
	addAttr -is true -ci true -sn "CavityTexture1G" -ln "CavityTexture1G" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "CavityTexture1";
	addAttr -is true -ci true -sn "CavityTexture1B" -ln "CavityTexture1B" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "CavityTexture1";
	addAttr -is true -ci true -h true -sn "Mask1__Name" -ln "Mask1__Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask1__Type" -ln "Mask1__Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -uac -sn "Mask1_" -ln "Mask1_" -nn "Mask Map 1" -ct "HW_shader_parameter" 
		-at "float3" -nc 3;
	addAttr -is true -ci true -sn "Mask1_R" -ln "Mask1_R" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "Mask1_";
	addAttr -is true -ci true -sn "Mask1_G" -ln "Mask1_G" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "Mask1_";
	addAttr -is true -ci true -sn "Mask1_B" -ln "Mask1_B" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "Mask1_";
	addAttr -is true -ci true -h true -sn "Mask2__Name" -ln "Mask2__Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask2__Type" -ln "Mask2__Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -uac -sn "Mask2_" -ln "Mask2_" -nn "Mask Map 2" -ct "HW_shader_parameter" 
		-at "float3" -nc 3;
	addAttr -is true -ci true -sn "Mask2_R" -ln "Mask2_R" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "Mask2_";
	addAttr -is true -ci true -sn "Mask2_G" -ln "Mask2_G" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "Mask2_";
	addAttr -is true -ci true -sn "Mask2_B" -ln "Mask2_B" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "Mask2_";
	addAttr -is true -ci true -h true -sn "Mask3__Name" -ln "Mask3__Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask3__Type" -ln "Mask3__Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -uac -sn "Mask3_" -ln "Mask3_" -nn "Mask Map 3" -ct "HW_shader_parameter" 
		-at "float3" -nc 3;
	addAttr -is true -ci true -sn "Mask3_R" -ln "Mask3_R" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "Mask3_";
	addAttr -is true -ci true -sn "Mask3_G" -ln "Mask3_G" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "Mask3_";
	addAttr -is true -ci true -sn "Mask3_B" -ln "Mask3_B" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "Mask3_";
	addAttr -is true -ci true -h true -sn "Mask4__Name" -ln "Mask4__Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask4__Type" -ln "Mask4__Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -uac -sn "Mask4_" -ln "Mask4_" -nn "Mask Map 4" -ct "HW_shader_parameter" 
		-at "float3" -nc 3;
	addAttr -is true -ci true -sn "Mask4_R" -ln "Mask4_R" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "Mask4_";
	addAttr -is true -ci true -sn "Mask4_G" -ln "Mask4_G" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "Mask4_";
	addAttr -is true -ci true -sn "Mask4_B" -ln "Mask4_B" -ct "HW_shader_parameter" 
		-smn 0 -smx 1 -at "float" -p "Mask4_";
	addAttr -is true -ci true -h true -sn "Mask1_Name" -ln "Mask1_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask1_Type" -ln "Mask1_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask1" -ln "Mask1" -nn "Mask 1" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask2_Name" -ln "Mask2_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask2_Type" -ln "Mask2_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask2" -ln "Mask2" -nn "Mask 2" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask3_Name" -ln "Mask3_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask3_Type" -ln "Mask3_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask3" -ln "Mask3" -nn "Mask 3" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask4_Name" -ln "Mask4_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask4_Type" -ln "Mask4_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask4" -ln "Mask4" -nn "Mask 4" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask5_Name" -ln "Mask5_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask5_Type" -ln "Mask5_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask5" -ln "Mask5" -nn "Mask 5" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask6_Name" -ln "Mask6_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask6_Type" -ln "Mask6_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask6" -ln "Mask6" -nn "Mask 6" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask7_Name" -ln "Mask7_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask7_Type" -ln "Mask7_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask7" -ln "Mask7" -nn "Mask 7" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask8_Name" -ln "Mask8_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask8_Type" -ln "Mask8_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask8" -ln "Mask8" -nn "Mask 8" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask9_Name" -ln "Mask9_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask9_Type" -ln "Mask9_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask9" -ln "Mask9" -nn "Mask 9" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask10_Name" -ln "Mask10_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask10_Type" -ln "Mask10_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask10" -ln "Mask10" -nn "Mask 10" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask11_Name" -ln "Mask11_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask11_Type" -ln "Mask11_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask11" -ln "Mask11" -nn "Mask 11" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask12_Name" -ln "Mask12_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask12_Type" -ln "Mask12_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask12" -ln "Mask12" -nn "Mask 12" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask13_Name" -ln "Mask13_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask13_Type" -ln "Mask13_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask13" -ln "Mask13" -nn "Mask 13" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask14_Name" -ln "Mask14_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask14_Type" -ln "Mask14_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask14" -ln "Mask14" -nn "Mask 14" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask15_Name" -ln "Mask15_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask15_Type" -ln "Mask15_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask15" -ln "Mask15" -nn "Mask 15" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask16_Name" -ln "Mask16_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask16_Type" -ln "Mask16_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask16" -ln "Mask16" -nn "Mask 16" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask17_Name" -ln "Mask17_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask17_Type" -ln "Mask17_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask17" -ln "Mask17" -nn "Mask 17" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask18_Name" -ln "Mask18_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask18_Type" -ln "Mask18_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask18" -ln "Mask18" -nn "Mask 18" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask19_Name" -ln "Mask19_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask19_Type" -ln "Mask19_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask19" -ln "Mask19" -nn "Mask 19" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask20_Name" -ln "Mask20_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask20_Type" -ln "Mask20_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask20" -ln "Mask20" -nn "Mask 20" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask21_Name" -ln "Mask21_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask21_Type" -ln "Mask21_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask21" -ln "Mask21" -nn "Mask 21" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask22_Name" -ln "Mask22_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask22_Type" -ln "Mask22_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask22" -ln "Mask22" -nn "Mask 22" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask23_Name" -ln "Mask23_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask23_Type" -ln "Mask23_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask23" -ln "Mask23" -nn "Mask 23" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask24_Name" -ln "Mask24_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask24_Type" -ln "Mask24_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask24" -ln "Mask24" -nn "Mask 24" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask25_Name" -ln "Mask25_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask25_Type" -ln "Mask25_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask25" -ln "Mask25" -nn "Mask 25" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask26_Name" -ln "Mask26_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask26_Type" -ln "Mask26_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask26" -ln "Mask26" -nn "Mask 26" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask27_Name" -ln "Mask27_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask27_Type" -ln "Mask27_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask27" -ln "Mask27" -nn "Mask 27" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask28_Name" -ln "Mask28_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask28_Type" -ln "Mask28_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask28" -ln "Mask28" -nn "Mask 28" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask29_Name" -ln "Mask29_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask29_Type" -ln "Mask29_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask29" -ln "Mask29" -nn "Mask 29" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask30_Name" -ln "Mask30_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask30_Type" -ln "Mask30_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask30" -ln "Mask30" -nn "Mask 30" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask31_Name" -ln "Mask31_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask31_Type" -ln "Mask31_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask31" -ln "Mask31" -nn "Mask 31" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask32_Name" -ln "Mask32_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask32_Type" -ln "Mask32_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask32" -ln "Mask32" -nn "Mask 32" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask33_Name" -ln "Mask33_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask33_Type" -ln "Mask33_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask33" -ln "Mask33" -nn "Mask 33" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask34_Name" -ln "Mask34_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask34_Type" -ln "Mask34_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask34" -ln "Mask34" -nn "Mask 34" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask35_Name" -ln "Mask35_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask35_Type" -ln "Mask35_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask35" -ln "Mask35" -nn "Mask 35" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask36_Name" -ln "Mask36_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask36_Type" -ln "Mask36_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask36" -ln "Mask36" -nn "Mask 36" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask37_Name" -ln "Mask37_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask37_Type" -ln "Mask37_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask37" -ln "Mask37" -nn "Mask 37" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask38_Name" -ln "Mask38_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask38_Type" -ln "Mask38_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask38" -ln "Mask38" -nn "Mask 38" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask39_Name" -ln "Mask39_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask39_Type" -ln "Mask39_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask39" -ln "Mask39" -nn "Mask 39" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask40_Name" -ln "Mask40_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask40_Type" -ln "Mask40_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask40" -ln "Mask40" -nn "Mask 40" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask41_Name" -ln "Mask41_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask41_Type" -ln "Mask41_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask41" -ln "Mask41" -nn "Mask 41" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask42_Name" -ln "Mask42_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask42_Type" -ln "Mask42_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask42" -ln "Mask42" -nn "Mask 42" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask43_Name" -ln "Mask43_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask43_Type" -ln "Mask43_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask43" -ln "Mask43" -nn "Mask 43" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask44_Name" -ln "Mask44_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask44_Type" -ln "Mask44_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask44" -ln "Mask44" -nn "Mask 44" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask45_Name" -ln "Mask45_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask45_Type" -ln "Mask45_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask45" -ln "Mask45" -nn "Mask 45" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask46_Name" -ln "Mask46_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask46_Type" -ln "Mask46_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask46" -ln "Mask46" -nn "Mask 46" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask47_Name" -ln "Mask47_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask47_Type" -ln "Mask47_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask47" -ln "Mask47" -nn "Mask 47" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Mask48_Name" -ln "Mask48_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Mask48_Type" -ln "Mask48_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Mask48" -ln "Mask48" -nn "Mask 48" -ct "HW_shader_parameter" 
		-min 0 -smx 5 -at "float";
	addAttr -is true -ci true -h true -sn "Redness_Name" -ln "Redness_Name" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -h true -sn "Redness_Type" -ln "Redness_Type" -ct "HW_shader_parameter" 
		-dt "string";
	addAttr -is true -ci true -k true -sn "Redness" -ln "Redness" -nn "Redness" -ct "HW_shader_parameter" 
		-dv 0.89999997615814209 -min 0 -smx 1 -at "float";
	setAttr ".vpar" -type "stringArray" 7 "Position" "TexCoord0" "TexCoord1" "TexCoord2" "Normal" "Binormal0" "Tangent0"  ;
	setAttr ".upar" -type "stringArray" 201 "SuperFilterTaps" "shadowMapTexelSize" "IsSwatchRender" "MayaFullScreenGamma" "LinearSpaceLighting" "UseShadows" "shadowMultiplier" "shadowDepthBias" "flipBackfaceNormals" "ShadowColor" "ShadowSpread" "ShadowSamples" "light0Enable" "light0Type" "light0Pos" "light0Color" "light0Intensity" "light0Dir" "light0ConeAngle" "light0FallOff" "light0AttenScale" "light0ShadowOn" "light1Enable" "light1Type" "light1Pos" "light1Color" "light1Intensity" "light1Dir" "light1ConeAngle" "light1FallOff" "light1AttenScale" "light1ShadowOn" "light2Enable" "light2Type" "light2Pos" "light2Color" "light2Intensity" "light2Dir" "light2ConeAngle" "light2FallOff" "light2AttenScale" "light2ShadowOn" "rimFresnelMin" "rimFresnelMax" "rimBrightness" "UseEmissiveTexture" "EmissiveTexture" "EmissiveIntensity" "AmbientSkyColor" "AmbientGroundColor" "UseAmbientOcclusionTexture" "AmbientOcclusionTexture" "DiffuseModel" "UseDiffuseTexture" "UseDiffuseTextureAlpha" "DiffuseTexture" "DiffuseColor" "Opacity" "UseOpacityMaskTexture" "OpacityMaskTexture" "OpacityMaskBias" "OpacityFresnelMin" "OpacityFresnelMax" "UseLightmapTexture" "LightmapTexture" "SpecularModel" "UseSpecularTexture" "SpecularTexture" "SpecularColor" "SpecPower" "SpecularColor2" "UseAnisotropicDirectionMap" "AnisotropicDirectionType" "SpecPower2" "AnisotropicTexture" "AnisotropicSpecularColor" "AnisotropicRoughness1" "UseAnisotropicMapAlphaMask" "UseNormalTexture" "NormalTexture" "NormalHeight" "SupportNonUniformScale" "NormalCoordsysX" "NormalCoordsysY" "CompExpTexture1" "CavityTexture1" "Mask1_" "Mask2_" "Mask3_" "Mask4_" "Mask1" "Mask2" "Mask3" "Mask4" "Mask5" "Mask6" "Mask7" "Mask8" "Mask9" "Mask10" "Mask11" "Mask12" "Mask13" "Mask14" "Mask15" "Mask16" "Mask17" "Mask18" "Mask19" "Mask20" "Mask21" "Mask22" "Mask23" "Mask24" "Mask25" "Mask26" "Mask27" "Mask28" "Mask29" "Mask30" "Mask31" "Mask32" "Mask33" "Mask34" "Mask35" "Mask36" "Mask37" "Mask38" "Mask39" "Mask40" "Mask41" "Mask42" "Mask43" "Mask44" "Mask45" "Mask46" "Mask47" "Mask48" "UseReflectionMap" "ReflectionType" "ReflectionTextureCube" "ReflectionTexture2D" "ReflectionIntensity" "ReflectionBlur" "ReflectionRotation" "ReflectionPinching" "ReflectionFresnelMin" "ReflectionFresnelMax" "UseReflectionMask" "ReflectionMask" "UseSpecAlphaForReflectionBlur" "UseSpecColorToTintReflection" "ReflectionAffectOpacity" "DisplacementModel" "UseDisplacementMap" "DisplacementTexture" "VectorDisplacementCoordSys" "DisplacementHeight" "DisplacementOffset" "DisplacementClippingBias" "BBoxExtraScale" "TessellationRange" "TessellationMin" "FlatTessellation" "UseTranslucency" "UseThicknessTexture" "TranslucencyThicknessMask" "translucentDistortion" "translucentPower" "translucentScale" "translucentMin" "SkinRampOuterColor" "SkinRampMediumColor" "SkinRampInnerColor" "UseBlendedNormalTexture" "BlendedNormalMask" "blendNorm" "Redness" "UseDiffuseIBLMap" "DiffuseIBLTextureCube" "DiffuseIBLTexture2D" "DiffuseIBLType" "DiffuseIBLIntensity" "DiffuseIBLBlur" "DiffuseIBLRotation" "DiffuseIBLPinching" "EmissiveTexcoord" "DiffuseTexcoord" "AmbientOcclusionTexcoord" "LightmapTexcoord" "BlendedNormalMaskTexcoord" "OpacityMaskTexcoord" "SpecularTexcoord" "AnisotropicTexcoord" "NormalTexcoord" "ReflectionMaskTexcoord" "DisplacementTexcoord" "ThicknessTexcoord" "light0ShadowMap" "light1ShadowMap" "light2ShadowMap"  ;
	setAttr ".s" -type "string" "I:/proj/mopian_immortal_epi/syncData/workgroup/RIG_WorkGrp/ExternalTeam/DX11/SkinShader_Maya_9.fx";
	setAttr ".t" -type "string" "SkinShader";
	setAttr ".SuperFilterTaps_Name" -type "string" "SuperFilterTaps";
	setAttr ".SuperFilterTaps_Type" -type "string" "float1x2";
	setAttr ".SuperFilterTaps" -type "float2" 0.48207608 -0.32157996 ;
	setAttr ".shadowMapTexelSize_Name" -type "string" "shadowMapTexelSize";
	setAttr ".shadowMapTexelSize_Type" -type "string" "float";
	setAttr ".shadowMapTexelSize" 0.0019531298894435167;
	setAttr ".LinearSpaceLighting_Name" -type "string" "LinearSpaceLighting";
	setAttr ".LinearSpaceLighting_Type" -type "string" "bool";
	setAttr ".LinearSpaceLighting" no;
	setAttr ".UseShadows_Name" -type "string" "UseShadows";
	setAttr ".UseShadows_Type" -type "string" "bool";
	setAttr -k on ".UseShadows" yes;
	setAttr ".shadowMultiplier_Name" -type "string" "shadowMultiplier";
	setAttr ".shadowMultiplier_Type" -type "string" "float";
	setAttr -k on ".shadowMultiplier" 1;
	setAttr ".IsSwatchRender_Name" -type "string" "IsSwatchRender";
	setAttr ".IsSwatchRender_Type" -type "string" "bool";
	setAttr ".IsSwatchRender" no;
	setAttr ".shadowDepthBias_Name" -type "string" "shadowDepthBias";
	setAttr ".shadowDepthBias_Type" -type "string" "float";
	setAttr -k on ".shadowDepthBias" 0.0099999997764825821;
	setAttr ".MayaFullScreenGamma_Name" -type "string" "MayaFullScreenGamma";
	setAttr ".MayaFullScreenGamma_Type" -type "string" "bool";
	setAttr ".MayaFullScreenGamma" no;
	setAttr ".flipBackfaceNormals_Name" -type "string" "flipBackfaceNormals";
	setAttr ".flipBackfaceNormals_Type" -type "string" "bool";
	setAttr -k on ".flipBackfaceNormals" yes;
	setAttr ".light0Enable_Name" -type "string" "light0Enable";
	setAttr ".light0Enable_Type" -type "string" "bool";
	setAttr -k on ".light0Enable" no;
	setAttr ".light0Type_Name" -type "string" "light0Type";
	setAttr ".light0Type_Type" -type "string" "enum";
	setAttr -k on ".light0Type" 2;
	setAttr ".light0Pos_Name" -type "string" "light0Pos";
	setAttr ".light0Pos_Type" -type "string" "matrix1x3";
	setAttr -k on ".light0Pos" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 100 100 100 1;
	setAttr ".light0Color_Name" -type "string" "light0Color";
	setAttr ".light0Color_Type" -type "string" "color1x3";
	setAttr -k on ".light0Color" -type "float3" 1 1 1 ;
	setAttr ".light0Intensity_Name" -type "string" "light0Intensity";
	setAttr ".light0Intensity_Type" -type "string" "float";
	setAttr -k on ".light0Intensity" 1;
	setAttr ".light0Dir_Name" -type "string" "light0Dir";
	setAttr ".light0Dir_Type" -type "string" "matrix1x3";
	setAttr -k on ".light0Dir" -type "matrix" 1 0 0 0 0 1 0 0 -100 -100 -100 0 0 0 0 1;
	setAttr ".light0ConeAngle_Name" -type "string" "light0ConeAngle";
	setAttr ".light0ConeAngle_Type" -type "string" "float";
	setAttr -k on ".light0ConeAngle" 0.46000000834465027;
	setAttr ".light0FallOff_Name" -type "string" "light0FallOff";
	setAttr ".light0FallOff_Type" -type "string" "float";
	setAttr -k on ".light0FallOff" 0.69999998807907104;
	setAttr ".light0AttenScale_Name" -type "string" "light0AttenScale";
	setAttr ".light0AttenScale_Type" -type "string" "float";
	setAttr -k on ".light0AttenScale" 0;
	setAttr ".light0ShadowOn_Name" -type "string" "light0ShadowOn";
	setAttr ".light0ShadowOn_Type" -type "string" "bool";
	setAttr ".light0ShadowOn" yes;
	setAttr ".light1Enable_Name" -type "string" "light1Enable";
	setAttr ".light1Enable_Type" -type "string" "bool";
	setAttr -k on ".light1Enable" no;
	setAttr ".light1Type_Name" -type "string" "light1Type";
	setAttr ".light1Type_Type" -type "string" "enum";
	setAttr -k on ".light1Type" 2;
	setAttr ".light1Pos_Name" -type "string" "light1Pos";
	setAttr ".light1Pos_Type" -type "string" "matrix1x3";
	setAttr -k on ".light1Pos" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -100 100 100 1;
	setAttr ".light1Color_Name" -type "string" "light1Color";
	setAttr ".light1Color_Type" -type "string" "color1x3";
	setAttr -k on ".light1Color" -type "float3" 1 1 1 ;
	setAttr ".light1Intensity_Name" -type "string" "light1Intensity";
	setAttr ".light1Intensity_Type" -type "string" "float";
	setAttr -k on ".light1Intensity" 1;
	setAttr ".light1Dir_Name" -type "string" "light1Dir";
	setAttr ".light1Dir_Type" -type "string" "matrix1x3";
	setAttr -k on ".light1Dir" -type "matrix" 1 0 0 0 0 1 0 0 -100 -100 -100 0 0 0 0 1;
	setAttr ".light1ConeAngle_Name" -type "string" "light1ConeAngle";
	setAttr ".light1ConeAngle_Type" -type "string" "float";
	setAttr -k on ".light1ConeAngle" 45;
	setAttr ".light1FallOff_Name" -type "string" "light1FallOff";
	setAttr ".light1FallOff_Type" -type "string" "float";
	setAttr -k on ".light1FallOff" 0;
	setAttr ".light1AttenScale_Name" -type "string" "light1AttenScale";
	setAttr ".light1AttenScale_Type" -type "string" "float";
	setAttr -k on ".light1AttenScale" 0;
	setAttr ".light1ShadowOn_Name" -type "string" "light1ShadowOn";
	setAttr ".light1ShadowOn_Type" -type "string" "bool";
	setAttr ".light1ShadowOn" yes;
	setAttr ".light2Enable_Name" -type "string" "light2Enable";
	setAttr ".light2Enable_Type" -type "string" "bool";
	setAttr -k on ".light2Enable" no;
	setAttr ".light2Type_Name" -type "string" "light2Type";
	setAttr ".light2Type_Type" -type "string" "enum";
	setAttr -k on ".light2Type" 2;
	setAttr ".light2Pos_Name" -type "string" "light2Pos";
	setAttr ".light2Pos_Type" -type "string" "matrix1x3";
	setAttr -k on ".light2Pos" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 100 100 -100 1;
	setAttr ".light2Color_Name" -type "string" "light2Color";
	setAttr ".light2Color_Type" -type "string" "color1x3";
	setAttr -k on ".light2Color" -type "float3" 1 1 1 ;
	setAttr ".light2Intensity_Name" -type "string" "light2Intensity";
	setAttr ".light2Intensity_Type" -type "string" "float";
	setAttr -k on ".light2Intensity" 1;
	setAttr ".light2Dir_Name" -type "string" "light2Dir";
	setAttr ".light2Dir_Type" -type "string" "matrix1x3";
	setAttr -k on ".light2Dir" -type "matrix" 1 0 0 0 0 1 0 0 -100 -100 -100 0 0 0 0 1;
	setAttr ".light2ConeAngle_Name" -type "string" "light2ConeAngle";
	setAttr ".light2ConeAngle_Type" -type "string" "float";
	setAttr -k on ".light2ConeAngle" 45;
	setAttr ".light2FallOff_Name" -type "string" "light2FallOff";
	setAttr ".light2FallOff_Type" -type "string" "float";
	setAttr -k on ".light2FallOff" 0;
	setAttr ".light2AttenScale_Name" -type "string" "light2AttenScale";
	setAttr ".light2AttenScale_Type" -type "string" "float";
	setAttr -k on ".light2AttenScale" 0;
	setAttr ".light2ShadowOn_Name" -type "string" "light2ShadowOn";
	setAttr ".light2ShadowOn_Type" -type "string" "bool";
	setAttr ".light2ShadowOn" yes;
	setAttr ".rimFresnelMin_Name" -type "string" "rimFresnelMin";
	setAttr ".rimFresnelMin_Type" -type "string" "float";
	setAttr -k on ".rimFresnelMin" 0.80000001192092896;
	setAttr ".rimFresnelMax_Name" -type "string" "rimFresnelMax";
	setAttr ".rimFresnelMax_Type" -type "string" "float";
	setAttr -k on ".rimFresnelMax" 1;
	setAttr ".rimBrightness_Name" -type "string" "rimBrightness";
	setAttr ".rimBrightness_Type" -type "string" "float";
	setAttr -k on ".rimBrightness" 0;
	setAttr ".UseEmissiveTexture_Name" -type "string" "UseEmissiveTexture";
	setAttr ".UseEmissiveTexture_Type" -type "string" "bool";
	setAttr -k on ".UseEmissiveTexture" no;
	setAttr ".EmissiveTexture_Name" -type "string" "EmissiveTexture";
	setAttr ".EmissiveTexture_Type" -type "string" "texture";
	setAttr ".EmissiveTexture" -type "float3" 0 0 0 ;
	setAttr ".EmissiveIntensity_Name" -type "string" "EmissiveIntensity";
	setAttr ".EmissiveIntensity_Type" -type "string" "float";
	setAttr -k on ".EmissiveIntensity" 1;
	setAttr ".AmbientSkyColor_Name" -type "string" "AmbientSkyColor";
	setAttr ".AmbientSkyColor_Type" -type "string" "color1x3";
	setAttr -k on ".AmbientSkyColor" -type "float3" 0 0 0 ;
	setAttr ".AmbientGroundColor_Name" -type "string" "AmbientGroundColor";
	setAttr ".AmbientGroundColor_Type" -type "string" "color1x3";
	setAttr -k on ".AmbientGroundColor" -type "float3" 0 0 0 ;
	setAttr ".AmbientOcclusionTexture_Name" -type "string" "AmbientOcclusionTexture";
	setAttr ".AmbientOcclusionTexture_Type" -type "string" "texture";
	setAttr ".AmbientOcclusionTexture" -type "float3" 0 0 0 ;
	setAttr ".UseAmbientOcclusionTexture_Name" -type "string" "UseAmbientOcclusionTexture";
	setAttr ".UseAmbientOcclusionTexture_Type" -type "string" "bool";
	setAttr -k on ".UseAmbientOcclusionTexture" no;
	setAttr ".DiffuseModel_Name" -type "string" "DiffuseModel";
	setAttr ".DiffuseModel_Type" -type "string" "enum";
	setAttr ".DiffuseModel" 0;
	setAttr ".UseDiffuseTexture_Name" -type "string" "UseDiffuseTexture";
	setAttr ".UseDiffuseTexture_Type" -type "string" "bool";
	setAttr -k on ".UseDiffuseTexture" yes;
	setAttr ".UseDiffuseTextureAlpha_Name" -type "string" "UseDiffuseTextureAlpha";
	setAttr ".UseDiffuseTextureAlpha_Type" -type "string" "bool";
	setAttr ".UseDiffuseTextureAlpha" no;
	setAttr ".DiffuseTexture_Name" -type "string" "DiffuseTexture";
	setAttr ".DiffuseTexture_Type" -type "string" "texture";
	setAttr ".DiffuseTexture" -type "float3" 0 0 0 ;
	setAttr ".DiffuseColor_Name" -type "string" "DiffuseColor";
	setAttr ".DiffuseColor_Type" -type "string" "color1x3";
	setAttr -k on ".DiffuseColor" -type "float3" 1 1 1 ;
	setAttr ".Opacity_Name" -type "string" "Opacity";
	setAttr ".Opacity_Type" -type "string" "float";
	setAttr ".Opacity" 1;
	setAttr ".UseOpacityMaskTexture_Name" -type "string" "UseOpacityMaskTexture";
	setAttr ".UseOpacityMaskTexture_Type" -type "string" "bool";
	setAttr ".UseOpacityMaskTexture" no;
	setAttr ".OpacityMaskTexture_Name" -type "string" "OpacityMaskTexture";
	setAttr ".OpacityMaskTexture_Type" -type "string" "texture";
	setAttr ".OpacityMaskTexture" -type "float3" 0 0 0 ;
	setAttr ".OpacityMaskBias_Name" -type "string" "OpacityMaskBias";
	setAttr ".OpacityMaskBias_Type" -type "string" "float";
	setAttr ".OpacityMaskBias" 0.10000000149011612;
	setAttr ".OpacityFresnelMin_Name" -type "string" "OpacityFresnelMin";
	setAttr ".OpacityFresnelMin_Type" -type "string" "float";
	setAttr ".OpacityFresnelMin" 0;
	setAttr ".OpacityFresnelMax_Name" -type "string" "OpacityFresnelMax";
	setAttr ".OpacityFresnelMax_Type" -type "string" "float";
	setAttr ".OpacityFresnelMax" 0;
	setAttr ".UseLightmapTexture_Name" -type "string" "UseLightmapTexture";
	setAttr ".UseLightmapTexture_Type" -type "string" "bool";
	setAttr ".UseLightmapTexture" no;
	setAttr ".LightmapTexture_Name" -type "string" "LightmapTexture";
	setAttr ".LightmapTexture_Type" -type "string" "texture";
	setAttr ".LightmapTexture" -type "float3" 0 0 0 ;
	setAttr ".SpecularModel_Name" -type "string" "SpecularModel";
	setAttr ".SpecularModel_Type" -type "string" "enum";
	setAttr ".SpecularModel" 0;
	setAttr ".UseSpecularTexture_Name" -type "string" "UseSpecularTexture";
	setAttr ".UseSpecularTexture_Type" -type "string" "bool";
	setAttr -k on ".UseSpecularTexture" no;
	setAttr ".SpecularTexture_Name" -type "string" "SpecularTexture";
	setAttr ".SpecularTexture_Type" -type "string" "texture";
	setAttr ".SpecularTexture" -type "float3" 0 0 0 ;
	setAttr ".SpecularColor_Name" -type "string" "SpecularColor";
	setAttr ".SpecularColor_Type" -type "string" "color1x3";
	setAttr -k on ".SpecularColor" -type "float3" 1 1 1 ;
	setAttr ".SpecPower_Name" -type "string" "SpecPower";
	setAttr ".SpecPower_Type" -type "string" "float";
	setAttr -k on ".SpecPower" 80;
	setAttr ".UseAnisotropicDirectionMap_Name" -type "string" "UseAnisotropicDirectionMap";
	setAttr ".UseAnisotropicDirectionMap_Type" -type "string" "bool";
	setAttr ".UseAnisotropicDirectionMap" no;
	setAttr ".AnisotropicDirectionType_Name" -type "string" "AnisotropicDirectionType";
	setAttr ".AnisotropicDirectionType_Type" -type "string" "enum";
	setAttr ".AnisotropicDirectionType" 0;
	setAttr ".AnisotropicTexture_Name" -type "string" "AnisotropicTexture";
	setAttr ".AnisotropicTexture_Type" -type "string" "texture";
	setAttr ".AnisotropicTexture" -type "float3" 0 0 0 ;
	setAttr ".AnisotropicRoughness1_Name" -type "string" "AnisotropicRoughness1";
	setAttr ".AnisotropicRoughness1_Type" -type "string" "float";
	setAttr ".AnisotropicRoughness1" 0.20000000298023224;
	setAttr ".UseAnisotropicMapAlphaMask_Name" -type "string" "UseAnisotropicMapAlphaMask";
	setAttr ".UseAnisotropicMapAlphaMask_Type" -type "string" "bool";
	setAttr ".UseAnisotropicMapAlphaMask" no;
	setAttr ".UseNormalTexture_Name" -type "string" "UseNormalTexture";
	setAttr ".UseNormalTexture_Type" -type "string" "bool";
	setAttr -k on ".UseNormalTexture" yes;
	setAttr ".NormalTexture_Name" -type "string" "NormalTexture";
	setAttr ".NormalTexture_Type" -type "string" "texture";
	setAttr ".NormalTexture" -type "float3" 0 0 0 ;
	setAttr ".NormalHeight_Name" -type "string" "NormalHeight";
	setAttr ".NormalHeight_Type" -type "string" "float";
	setAttr -k on ".NormalHeight" 1;
	setAttr ".SupportNonUniformScale_Name" -type "string" "SupportNonUniformScale";
	setAttr ".SupportNonUniformScale_Type" -type "string" "bool";
	setAttr -k on ".SupportNonUniformScale" yes;
	setAttr ".NormalCoordsysX_Name" -type "string" "NormalCoordsysX";
	setAttr ".NormalCoordsysX_Type" -type "string" "enum";
	setAttr -k on ".NormalCoordsysX" 0;
	setAttr ".NormalCoordsysY_Name" -type "string" "NormalCoordsysY";
	setAttr ".NormalCoordsysY_Type" -type "string" "enum";
	setAttr -k on ".NormalCoordsysY" 0;
	setAttr ".UseReflectionMap_Name" -type "string" "UseReflectionMap";
	setAttr ".UseReflectionMap_Type" -type "string" "bool";
	setAttr -k on ".UseReflectionMap" no;
	setAttr ".ReflectionType_Name" -type "string" "ReflectionType";
	setAttr ".ReflectionType_Type" -type "string" "enum";
	setAttr -k on ".ReflectionType" 0;
	setAttr ".ReflectionTextureCube_Name" -type "string" "ReflectionTextureCube";
	setAttr ".ReflectionTextureCube_Type" -type "string" "texture";
	setAttr ".ReflectionTextureCube" -type "float3" 0 0 0 ;
	setAttr ".ReflectionTexture2D_Name" -type "string" "ReflectionTexture2D";
	setAttr ".ReflectionTexture2D_Type" -type "string" "texture";
	setAttr ".ReflectionTexture2D" -type "float3" 0 0 0 ;
	setAttr ".ReflectionIntensity_Name" -type "string" "ReflectionIntensity";
	setAttr ".ReflectionIntensity_Type" -type "string" "float";
	setAttr -k on ".ReflectionIntensity" 0.20000000298023224;
	setAttr ".ReflectionBlur_Name" -type "string" "ReflectionBlur";
	setAttr ".ReflectionBlur_Type" -type "string" "float";
	setAttr -k on ".ReflectionBlur" 0;
	setAttr ".ReflectionRotation_Name" -type "string" "ReflectionRotation";
	setAttr ".ReflectionRotation_Type" -type "string" "float";
	setAttr -k on ".ReflectionRotation" 0;
	setAttr ".ReflectionPinching_Name" -type "string" "ReflectionPinching";
	setAttr ".ReflectionPinching_Type" -type "string" "float";
	setAttr -k on ".ReflectionPinching" 1.1000000238418579;
	setAttr ".ReflectionFresnelMin_Name" -type "string" "ReflectionFresnelMin";
	setAttr ".ReflectionFresnelMin_Type" -type "string" "float";
	setAttr -k on ".ReflectionFresnelMin" 0;
	setAttr ".ReflectionFresnelMax_Name" -type "string" "ReflectionFresnelMax";
	setAttr ".ReflectionFresnelMax_Type" -type "string" "float";
	setAttr -k on ".ReflectionFresnelMax" 0;
	setAttr ".UseReflectionMask_Name" -type "string" "UseReflectionMask";
	setAttr ".UseReflectionMask_Type" -type "string" "bool";
	setAttr -k on ".UseReflectionMask" no;
	setAttr ".ReflectionMask_Name" -type "string" "ReflectionMask";
	setAttr ".ReflectionMask_Type" -type "string" "texture";
	setAttr ".ReflectionMask" -type "float3" 0 0 0 ;
	setAttr ".UseSpecAlphaForReflectionBlur_Name" -type "string" "UseSpecAlphaForReflectionBlur";
	setAttr ".UseSpecAlphaForReflectionBlur_Type" -type "string" "bool";
	setAttr -k on ".UseSpecAlphaForReflectionBlur" no;
	setAttr ".UseSpecColorToTintReflection_Name" -type "string" "UseSpecColorToTintReflection";
	setAttr ".UseSpecColorToTintReflection_Type" -type "string" "bool";
	setAttr -k on ".UseSpecColorToTintReflection" no;
	setAttr ".ReflectionAffectOpacity_Name" -type "string" "ReflectionAffectOpacity";
	setAttr ".ReflectionAffectOpacity_Type" -type "string" "bool";
	setAttr -k on ".ReflectionAffectOpacity" yes;
	setAttr ".DisplacementModel_Name" -type "string" "DisplacementModel";
	setAttr ".DisplacementModel_Type" -type "string" "enum";
	setAttr ".DisplacementModel" 0;
	setAttr ".UseDisplacementMap_Name" -type "string" "UseDisplacementMap";
	setAttr ".UseDisplacementMap_Type" -type "string" "bool";
	setAttr ".UseDisplacementMap" no;
	setAttr ".DisplacementTexture_Name" -type "string" "DisplacementTexture";
	setAttr ".DisplacementTexture_Type" -type "string" "texture";
	setAttr ".DisplacementTexture" -type "float3" 0 0 0 ;
	setAttr ".VectorDisplacementCoordSys_Name" -type "string" "VectorDisplacementCoordSys";
	setAttr ".VectorDisplacementCoordSys_Type" -type "string" "enum";
	setAttr ".VectorDisplacementCoordSys" 0;
	setAttr ".DisplacementHeight_Name" -type "string" "DisplacementHeight";
	setAttr ".DisplacementHeight_Type" -type "string" "float";
	setAttr ".DisplacementHeight" 0.5;
	setAttr ".DisplacementOffset_Name" -type "string" "DisplacementOffset";
	setAttr ".DisplacementOffset_Type" -type "string" "float";
	setAttr ".DisplacementOffset" 0.5;
	setAttr ".DisplacementClippingBias_Name" -type "string" "DisplacementClippingBias";
	setAttr ".DisplacementClippingBias_Type" -type "string" "float";
	setAttr ".DisplacementClippingBias" 5;
	setAttr ".BBoxExtraScale_Name" -type "string" "BBoxExtraScale";
	setAttr ".BBoxExtraScale_Type" -type "string" "float";
	setAttr ".BBoxExtraScale" 1;
	setAttr ".TessellationRange_Name" -type "string" "TessellationRange";
	setAttr ".TessellationRange_Type" -type "string" "float";
	setAttr ".TessellationRange" 0;
	setAttr ".TessellationMin_Name" -type "string" "TessellationMin";
	setAttr ".TessellationMin_Type" -type "string" "float";
	setAttr ".TessellationMin" 3;
	setAttr ".FlatTessellation_Name" -type "string" "FlatTessellation";
	setAttr ".FlatTessellation_Type" -type "string" "float";
	setAttr ".FlatTessellation" 0;
	setAttr ".UseTranslucency_Name" -type "string" "UseTranslucency";
	setAttr ".UseTranslucency_Type" -type "string" "bool";
	setAttr ".UseTranslucency" no;
	setAttr ".UseThicknessTexture_Name" -type "string" "UseThicknessTexture";
	setAttr ".UseThicknessTexture_Type" -type "string" "bool";
	setAttr ".UseThicknessTexture" no;
	setAttr ".TranslucencyThicknessMask_Name" -type "string" "TranslucencyThicknessMask";
	setAttr ".TranslucencyThicknessMask_Type" -type "string" "texture";
	setAttr ".TranslucencyThicknessMask" -type "float3" 0 0 0 ;
	setAttr ".translucentDistortion_Name" -type "string" "translucentDistortion";
	setAttr ".translucentDistortion_Type" -type "string" "float";
	setAttr ".translucentDistortion" 0.20000000298023224;
	setAttr ".translucentPower_Name" -type "string" "translucentPower";
	setAttr ".translucentPower_Type" -type "string" "float";
	setAttr ".translucentPower" 3;
	setAttr ".translucentScale_Name" -type "string" "translucentScale";
	setAttr ".translucentScale_Type" -type "string" "float";
	setAttr ".translucentScale" 1;
	setAttr ".translucentMin_Name" -type "string" "translucentMin";
	setAttr ".translucentMin_Type" -type "string" "float";
	setAttr ".translucentMin" 0;
	setAttr ".SkinRampOuterColor_Name" -type "string" "SkinRampOuterColor";
	setAttr ".SkinRampOuterColor_Type" -type "string" "color1x3";
	setAttr ".SkinRampOuterColor" -type "float3" 1 0.63999999 0.25 ;
	setAttr ".SkinRampMediumColor_Name" -type "string" "SkinRampMediumColor";
	setAttr ".SkinRampMediumColor_Type" -type "string" "color1x3";
	setAttr ".SkinRampMediumColor" -type "float3" 1 0.20999999 0.14 ;
	setAttr ".SkinRampInnerColor_Name" -type "string" "SkinRampInnerColor";
	setAttr ".SkinRampInnerColor_Type" -type "string" "color1x3";
	setAttr ".SkinRampInnerColor" -type "float3" 0.25 0.050000001 0.02 ;
	setAttr ".UseBlendedNormalTexture_Name" -type "string" "UseBlendedNormalTexture";
	setAttr ".UseBlendedNormalTexture_Type" -type "string" "bool";
	setAttr -k on ".UseBlendedNormalTexture" no;
	setAttr ".BlendedNormalMask_Name" -type "string" "BlendedNormalMask";
	setAttr ".BlendedNormalMask_Type" -type "string" "texture";
	setAttr ".BlendedNormalMask" -type "float3" 0 0 0 ;
	setAttr ".blendNorm_Name" -type "string" "blendNorm";
	setAttr ".blendNorm_Type" -type "string" "float";
	setAttr -k on ".blendNorm" 0.15000000596046448;
	setAttr ".UseDiffuseIBLMap_Name" -type "string" "UseDiffuseIBLMap";
	setAttr ".UseDiffuseIBLMap_Type" -type "string" "bool";
	setAttr ".UseDiffuseIBLMap" no;
	setAttr ".DiffuseIBLTextureCube_Name" -type "string" "DiffuseIBLTextureCube";
	setAttr ".DiffuseIBLTextureCube_Type" -type "string" "texture";
	setAttr ".DiffuseIBLTextureCube" -type "float3" 0 0 0 ;
	setAttr ".DiffuseIBLTexture2D_Name" -type "string" "DiffuseIBLTexture2D";
	setAttr ".DiffuseIBLTexture2D_Type" -type "string" "texture";
	setAttr ".DiffuseIBLTexture2D" -type "float3" 0 0 0 ;
	setAttr ".DiffuseIBLType_Name" -type "string" "DiffuseIBLType";
	setAttr ".DiffuseIBLType_Type" -type "string" "enum";
	setAttr ".DiffuseIBLType" 0;
	setAttr ".DiffuseIBLIntensity_Name" -type "string" "DiffuseIBLIntensity";
	setAttr ".DiffuseIBLIntensity_Type" -type "string" "float";
	setAttr ".DiffuseIBLIntensity" 0.5;
	setAttr ".DiffuseIBLBlur_Name" -type "string" "DiffuseIBLBlur";
	setAttr ".DiffuseIBLBlur_Type" -type "string" "float";
	setAttr ".DiffuseIBLBlur" 5;
	setAttr ".DiffuseIBLRotation_Name" -type "string" "DiffuseIBLRotation";
	setAttr ".DiffuseIBLRotation_Type" -type "string" "float";
	setAttr ".DiffuseIBLRotation" 0;
	setAttr ".DiffuseIBLPinching_Name" -type "string" "DiffuseIBLPinching";
	setAttr ".DiffuseIBLPinching_Type" -type "string" "float";
	setAttr ".DiffuseIBLPinching" 1.1000000238418579;
	setAttr ".EmissiveTexcoord_Name" -type "string" "EmissiveTexcoord";
	setAttr ".EmissiveTexcoord_Type" -type "string" "enum";
	setAttr ".EmissiveTexcoord" 0;
	setAttr ".DiffuseTexcoord_Name" -type "string" "DiffuseTexcoord";
	setAttr ".DiffuseTexcoord_Type" -type "string" "enum";
	setAttr -k on ".DiffuseTexcoord" 0;
	setAttr ".LightmapTexcoord_Name" -type "string" "LightmapTexcoord";
	setAttr ".LightmapTexcoord_Type" -type "string" "enum";
	setAttr ".LightmapTexcoord" 1;
	setAttr ".AmbientOcclusionTexcoord_Name" -type "string" "AmbientOcclusionTexcoord";
	setAttr ".AmbientOcclusionTexcoord_Type" -type "string" "enum";
	setAttr ".AmbientOcclusionTexcoord" 1;
	setAttr ".BlendedNormalMaskTexcoord_Name" -type "string" "BlendedNormalMaskTexcoord";
	setAttr ".BlendedNormalMaskTexcoord_Type" -type "string" "enum";
	setAttr -k on ".BlendedNormalMaskTexcoord" 0;
	setAttr ".OpacityMaskTexcoord_Name" -type "string" "OpacityMaskTexcoord";
	setAttr ".OpacityMaskTexcoord_Type" -type "string" "enum";
	setAttr ".OpacityMaskTexcoord" 0;
	setAttr ".SpecularTexcoord_Name" -type "string" "SpecularTexcoord";
	setAttr ".SpecularTexcoord_Type" -type "string" "enum";
	setAttr -k on ".SpecularTexcoord" 0;
	setAttr ".AnisotropicTexcoord_Name" -type "string" "AnisotropicTexcoord";
	setAttr ".AnisotropicTexcoord_Type" -type "string" "enum";
	setAttr ".AnisotropicTexcoord" 0;
	setAttr ".NormalTexcoord_Name" -type "string" "NormalTexcoord";
	setAttr ".NormalTexcoord_Type" -type "string" "enum";
	setAttr -k on ".NormalTexcoord" 0;
	setAttr ".ReflectionMaskTexcoord_Name" -type "string" "ReflectionMaskTexcoord";
	setAttr ".ReflectionMaskTexcoord_Type" -type "string" "enum";
	setAttr ".ReflectionMaskTexcoord" 0;
	setAttr ".DisplacementTexcoord_Name" -type "string" "DisplacementTexcoord";
	setAttr ".DisplacementTexcoord_Type" -type "string" "enum";
	setAttr ".DisplacementTexcoord" 0;
	setAttr ".ThicknessTexcoord_Name" -type "string" "ThicknessTexcoord";
	setAttr ".ThicknessTexcoord_Type" -type "string" "enum";
	setAttr ".ThicknessTexcoord" 0;
	setAttr ".light0ShadowMap_Name" -type "string" "light0ShadowMap";
	setAttr ".light0ShadowMap_Type" -type "string" "texture";
	setAttr ".light0ShadowMap" -type "float3" 0 0 0 ;
	setAttr ".light1ShadowMap_Name" -type "string" "light1ShadowMap";
	setAttr ".light1ShadowMap_Type" -type "string" "texture";
	setAttr ".light1ShadowMap" -type "float3" 0 0 0 ;
	setAttr ".light2ShadowMap_Name" -type "string" "light2ShadowMap";
	setAttr ".light2ShadowMap_Type" -type "string" "texture";
	setAttr ".light2ShadowMap" -type "float3" 0 0 0 ;
	setAttr ".Position_Name" -type "string" "Position";
	setAttr ".Position_Source" -type "string" "position";
	setAttr ".TexCoord0_Name" -type "string" "TexCoord0";
	setAttr ".TexCoord0_Source" -type "string" "uv:map1";
	setAttr ".TexCoord0_DefaultTexture" -type "string" "Mask4_";
	setAttr ".TexCoord1_Name" -type "string" "TexCoord1";
	setAttr ".TexCoord1_Source" -type "string" "uv:map2";
	setAttr ".TexCoord1_DefaultTexture" -type "string" "Mask4_";
	setAttr ".TexCoord2_Name" -type "string" "TexCoord2";
	setAttr ".TexCoord2_Source" -type "string" "uv:map3";
	setAttr ".TexCoord2_DefaultTexture" -type "string" "Mask4_";
	setAttr ".Normal_Name" -type "string" "Normal";
	setAttr ".Normal_Source" -type "string" "normal";
	setAttr ".Binormal0_Name" -type "string" "Binormal0";
	setAttr ".Binormal0_Source" -type "string" "binormal:map1";
	setAttr ".Tangent0_Name" -type "string" "Tangent0";
	setAttr ".Tangent0_Source" -type "string" "tangent:map1";
	setAttr ".ShadowColor_Name" -type "string" "ShadowColor";
	setAttr ".ShadowColor_Type" -type "string" "color1x3";
	setAttr -k on ".ShadowColor" -type "float3" 0.2 0 0 ;
	setAttr ".ShadowSpread_Name" -type "string" "ShadowSpread";
	setAttr ".ShadowSpread_Type" -type "string" "float";
	setAttr -k on ".ShadowSpread" 1;
	setAttr ".ShadowSamples_Name" -type "string" "ShadowSamples";
	setAttr ".ShadowSamples_Type" -type "string" "float";
	setAttr -k on ".ShadowSamples" 60;
	setAttr ".SpecularColor2_Name" -type "string" "SpecularColor2";
	setAttr ".SpecularColor2_Type" -type "string" "color1x3";
	setAttr -k on ".SpecularColor2" -type "float3" 1 1 1 ;
	setAttr ".SpecPower2_Name" -type "string" "SpecPower2";
	setAttr ".SpecPower2_Type" -type "string" "float";
	setAttr -k on ".SpecPower2" 50;
	setAttr ".AnisotropicSpecularColor_Name" -type "string" "AnisotropicSpecularColor";
	setAttr ".AnisotropicSpecularColor_Type" -type "string" "color1x3";
	setAttr ".AnisotropicSpecularColor" -type "float3" 1 1 1 ;
	setAttr ".CompExpTexture1_Name" -type "string" "CompExpTexture1";
	setAttr ".CompExpTexture1_Type" -type "string" "texture";
	setAttr ".CompExpTexture1" -type "float3" 0 0 0 ;
	setAttr ".CavityTexture1_Name" -type "string" "CavityTexture1";
	setAttr ".CavityTexture1_Type" -type "string" "texture";
	setAttr ".CavityTexture1" -type "float3" 0 0 0 ;
	setAttr ".Mask1__Name" -type "string" "Mask1_";
	setAttr ".Mask1__Type" -type "string" "texture";
	setAttr ".Mask1_" -type "float3" 0 0 0 ;
	setAttr ".Mask2__Name" -type "string" "Mask2_";
	setAttr ".Mask2__Type" -type "string" "texture";
	setAttr ".Mask2_" -type "float3" 0 0 0 ;
	setAttr ".Mask3__Name" -type "string" "Mask3_";
	setAttr ".Mask3__Type" -type "string" "texture";
	setAttr ".Mask3_" -type "float3" 0 0 0 ;
	setAttr ".Mask4__Name" -type "string" "Mask4_";
	setAttr ".Mask4__Type" -type "string" "texture";
	setAttr ".Mask4_" -type "float3" 0 0 0 ;
	setAttr ".Mask1_Name" -type "string" "Mask1";
	setAttr ".Mask1_Type" -type "string" "float";
	setAttr -k on ".Mask1" 0;
	setAttr ".Mask2_Name" -type "string" "Mask2";
	setAttr ".Mask2_Type" -type "string" "float";
	setAttr -k on ".Mask2" 0;
	setAttr ".Mask3_Name" -type "string" "Mask3";
	setAttr ".Mask3_Type" -type "string" "float";
	setAttr -k on ".Mask3" 0;
	setAttr ".Mask4_Name" -type "string" "Mask4";
	setAttr ".Mask4_Type" -type "string" "float";
	setAttr -k on ".Mask4" 0;
	setAttr ".Mask5_Name" -type "string" "Mask5";
	setAttr ".Mask5_Type" -type "string" "float";
	setAttr -k on ".Mask5" 0;
	setAttr ".Mask6_Name" -type "string" "Mask6";
	setAttr ".Mask6_Type" -type "string" "float";
	setAttr -k on ".Mask6" 0;
	setAttr ".Mask7_Name" -type "string" "Mask7";
	setAttr ".Mask7_Type" -type "string" "float";
	setAttr -k on ".Mask7" 0;
	setAttr ".Mask8_Name" -type "string" "Mask8";
	setAttr ".Mask8_Type" -type "string" "float";
	setAttr -k on ".Mask8" 0;
	setAttr ".Mask9_Name" -type "string" "Mask9";
	setAttr ".Mask9_Type" -type "string" "float";
	setAttr -k on ".Mask9" 0;
	setAttr ".Mask10_Name" -type "string" "Mask10";
	setAttr ".Mask10_Type" -type "string" "float";
	setAttr -k on ".Mask10" 0;
	setAttr ".Mask11_Name" -type "string" "Mask11";
	setAttr ".Mask11_Type" -type "string" "float";
	setAttr -k on ".Mask11" 0;
	setAttr ".Mask12_Name" -type "string" "Mask12";
	setAttr ".Mask12_Type" -type "string" "float";
	setAttr -k on ".Mask12" 0;
	setAttr ".Mask13_Name" -type "string" "Mask13";
	setAttr ".Mask13_Type" -type "string" "float";
	setAttr -k on ".Mask13" 0;
	setAttr ".Mask14_Name" -type "string" "Mask14";
	setAttr ".Mask14_Type" -type "string" "float";
	setAttr -k on ".Mask14" 0;
	setAttr ".Mask15_Name" -type "string" "Mask15";
	setAttr ".Mask15_Type" -type "string" "float";
	setAttr -k on ".Mask15" 0;
	setAttr ".Mask16_Name" -type "string" "Mask16";
	setAttr ".Mask16_Type" -type "string" "float";
	setAttr -k on ".Mask16" 0;
	setAttr ".Mask17_Name" -type "string" "Mask17";
	setAttr ".Mask17_Type" -type "string" "float";
	setAttr -k on ".Mask17" 0;
	setAttr ".Mask18_Name" -type "string" "Mask18";
	setAttr ".Mask18_Type" -type "string" "float";
	setAttr -k on ".Mask18" 0;
	setAttr ".Mask19_Name" -type "string" "Mask19";
	setAttr ".Mask19_Type" -type "string" "float";
	setAttr -k on ".Mask19" 0;
	setAttr ".Mask20_Name" -type "string" "Mask20";
	setAttr ".Mask20_Type" -type "string" "float";
	setAttr -k on ".Mask20" 0;
	setAttr ".Mask21_Name" -type "string" "Mask21";
	setAttr ".Mask21_Type" -type "string" "float";
	setAttr -k on ".Mask21" 0;
	setAttr ".Mask22_Name" -type "string" "Mask22";
	setAttr ".Mask22_Type" -type "string" "float";
	setAttr -k on ".Mask22" 0;
	setAttr ".Mask23_Name" -type "string" "Mask23";
	setAttr ".Mask23_Type" -type "string" "float";
	setAttr -k on ".Mask23" 0;
	setAttr ".Mask24_Name" -type "string" "Mask24";
	setAttr ".Mask24_Type" -type "string" "float";
	setAttr -k on ".Mask24" 0;
	setAttr ".Mask25_Name" -type "string" "Mask25";
	setAttr ".Mask25_Type" -type "string" "float";
	setAttr -k on ".Mask25" 0;
	setAttr ".Mask26_Name" -type "string" "Mask26";
	setAttr ".Mask26_Type" -type "string" "float";
	setAttr -k on ".Mask26" 0;
	setAttr ".Mask27_Name" -type "string" "Mask27";
	setAttr ".Mask27_Type" -type "string" "float";
	setAttr -k on ".Mask27" 0;
	setAttr ".Mask28_Name" -type "string" "Mask28";
	setAttr ".Mask28_Type" -type "string" "float";
	setAttr -k on ".Mask28" 0;
	setAttr ".Mask29_Name" -type "string" "Mask29";
	setAttr ".Mask29_Type" -type "string" "float";
	setAttr -k on ".Mask29" 0;
	setAttr ".Mask30_Name" -type "string" "Mask30";
	setAttr ".Mask30_Type" -type "string" "float";
	setAttr -k on ".Mask30" 0;
	setAttr ".Mask31_Name" -type "string" "Mask31";
	setAttr ".Mask31_Type" -type "string" "float";
	setAttr -k on ".Mask31" 0;
	setAttr ".Mask32_Name" -type "string" "Mask32";
	setAttr ".Mask32_Type" -type "string" "float";
	setAttr -k on ".Mask32" 0;
	setAttr ".Mask33_Name" -type "string" "Mask33";
	setAttr ".Mask33_Type" -type "string" "float";
	setAttr -k on ".Mask33" 0;
	setAttr ".Mask34_Name" -type "string" "Mask34";
	setAttr ".Mask34_Type" -type "string" "float";
	setAttr -k on ".Mask34" 0;
	setAttr ".Mask35_Name" -type "string" "Mask35";
	setAttr ".Mask35_Type" -type "string" "float";
	setAttr -k on ".Mask35" 0;
	setAttr ".Mask36_Name" -type "string" "Mask36";
	setAttr ".Mask36_Type" -type "string" "float";
	setAttr -k on ".Mask36" 0;
	setAttr ".Mask37_Name" -type "string" "Mask37";
	setAttr ".Mask37_Type" -type "string" "float";
	setAttr -k on ".Mask37" 0;
	setAttr ".Mask38_Name" -type "string" "Mask38";
	setAttr ".Mask38_Type" -type "string" "float";
	setAttr -k on ".Mask38" 0;
	setAttr ".Mask39_Name" -type "string" "Mask39";
	setAttr ".Mask39_Type" -type "string" "float";
	setAttr -k on ".Mask39" 0;
	setAttr ".Mask40_Name" -type "string" "Mask40";
	setAttr ".Mask40_Type" -type "string" "float";
	setAttr -k on ".Mask40" 0;
	setAttr ".Mask41_Name" -type "string" "Mask41";
	setAttr ".Mask41_Type" -type "string" "float";
	setAttr -k on ".Mask41" 0;
	setAttr ".Mask42_Name" -type "string" "Mask42";
	setAttr ".Mask42_Type" -type "string" "float";
	setAttr -k on ".Mask42" 0;
	setAttr ".Mask43_Name" -type "string" "Mask43";
	setAttr ".Mask43_Type" -type "string" "float";
	setAttr -k on ".Mask43" 0;
	setAttr ".Mask44_Name" -type "string" "Mask44";
	setAttr ".Mask44_Type" -type "string" "float";
	setAttr -k on ".Mask44" 0;
	setAttr ".Mask45_Name" -type "string" "Mask45";
	setAttr ".Mask45_Type" -type "string" "float";
	setAttr -k on ".Mask45" 0;
	setAttr ".Mask46_Name" -type "string" "Mask46";
	setAttr ".Mask46_Type" -type "string" "float";
	setAttr -k on ".Mask46" 0;
	setAttr ".Mask47_Name" -type "string" "Mask47";
	setAttr ".Mask47_Type" -type "string" "float";
	setAttr -k on ".Mask47" 0;
	setAttr ".Mask48_Name" -type "string" "Mask48";
	setAttr ".Mask48_Type" -type "string" "float";
	setAttr -k on ".Mask48" 0;
	setAttr ".Redness_Name" -type "string" "Redness";
	setAttr ".Redness_Type" -type "string" "float";
	setAttr -k on ".Redness" 0.89999997615814209;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "0E2F4E5C-4438-D02B-F8CE-4785E11C26D9";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanCgRigm 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n"
		+ "            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 4 4 \n            -bumpResolution 4 4 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n"
		+ "            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanCgRigm 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n"
		+ "            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 4 4 \n            -bumpResolution 4 4 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n"
		+ "            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanCgRigm 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n"
		+ "            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 4 4 \n            -bumpResolution 4 4 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n"
		+ "            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n"
		+ "            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanCgRigm 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n"
		+ "            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 1\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 4 4 \n            -bumpResolution 4 4 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n"
		+ "            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n"
		+ "            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1331\n            -height 746\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n"
		+ "            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n"
		+ "            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -selectCommand \"pass\" \n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n"
		+ "            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n"
		+ "                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n"
		+ "                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n"
		+ "                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 1\n                -outliner \"graphEditor1OutlineEd\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n"
		+ "                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n"
		+ "                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n"
		+ "                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n"
		+ "                -mergeConnections 0\n                -cgrigm 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n"
		+ "\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n"
		+ "                -editorMode \"default\" \n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n"
		+ "                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanCgRigm 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n"
		+ "                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererOverrideName \"stereoOverrideVP2\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n"
		+ "                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n"
		+ "                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n"
		+ "            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 0\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n"
		+ "            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -selectCommand \"look\" \n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Model Panel5\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tmodelPanel -edit -l (localizedPanelLabel(\"Model Panel5\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanCgRigm 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 1\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n"
		+ "            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 4 4 \n            -bumpResolution 4 4 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 0\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n"
		+ "            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1599\n            -height 746\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -docTag \\\"RADRENDER\\\" \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanCgRigm 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 1\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 4 4 \\n    -bumpResolution 4 4 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1331\\n    -height 746\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -docTag \\\"RADRENDER\\\" \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanCgRigm 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 1\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 4 4 \\n    -bumpResolution 4 4 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1331\\n    -height 746\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"1 0.000000 -1.000000 -0.000000 0.000000 0.000000 -1.000000\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "7613803A-49CA-C2D6-C75B-728D806CB6FC";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 58;
	setAttr -av -k on ".unw" 58;
	setAttr -av -k on ".etw";
	setAttr -av -k on ".tps";
	setAttr -av -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr -av -k on ".ihi";
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr -av ".ta";
	setAttr -av ".tq";
	setAttr -av ".aoam";
	setAttr -av ".aora";
	setAttr -av ".hfd";
	setAttr -av ".hfs";
	setAttr -av ".hfe";
	setAttr -av ".hfcr";
	setAttr -av ".hfcg";
	setAttr -av ".hfcb";
	setAttr -av ".hfa";
	setAttr -av ".mbe";
	setAttr -av -k on ".mbsof";
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -av -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -cb on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 3 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -cb on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -cb on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 5 ".s";
select -ne :postProcessList1;
	setAttr -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -cb on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 6 ".u";
select -ne :defaultRenderingList1;
	setAttr -k on ".ihi";
select -ne :defaultTextureList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 8 ".tx";
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".bbx";
	setAttr -k on ".vwm";
	setAttr -k on ".tpv";
	setAttr -k on ".uit";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -cb on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w";
	setAttr -av -k on ".h";
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar";
	setAttr -av -k on ".ldar";
	setAttr -av -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -av -k on ".isu";
	setAttr -av -k on ".pdu";
select -ne :hardwareRenderGlobals;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k off -cb on ".ctrs" 256;
	setAttr -av -k off -cb on ".btrs" 512;
	setAttr -k off -cb on ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off -cb on ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
connectAttr "dx11Shader8SG.msg" "materialInfo14.sg";
connectAttr "SkinShader.msg" "materialInfo14.m";
connectAttr "SkinShader.oc" "dx11Shader8SG.ss";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "dx11Shader8SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":hyperGraphLayout.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":defaultObjectSet.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":defaultHardwareRenderGlobals.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":initialShadingGroup.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "dx11Shader8SG.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr ":defaultColorMgtGlobals.cme" "face_dx11_wrinkle_normal.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "face_dx11_wrinkle_normal.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "face_dx11_wrinkle_normal.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "face_dx11_wrinkle_normal.ws";
connectAttr "face_dx11_wrinkle_normal_place2dTexture.c" "face_dx11_wrinkle_normal.c"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.tf" "face_dx11_wrinkle_normal.tf"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.rf" "face_dx11_wrinkle_normal.rf"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.mu" "face_dx11_wrinkle_normal.mu"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.mv" "face_dx11_wrinkle_normal.mv"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.s" "face_dx11_wrinkle_normal.s"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.wu" "face_dx11_wrinkle_normal.wu"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.wv" "face_dx11_wrinkle_normal.wv"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.re" "face_dx11_wrinkle_normal.re"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.of" "face_dx11_wrinkle_normal.of"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.r" "face_dx11_wrinkle_normal.ro"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.n" "face_dx11_wrinkle_normal.n"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.vt1" "face_dx11_wrinkle_normal.vt1"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.vt2" "face_dx11_wrinkle_normal.vt2"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.vt3" "face_dx11_wrinkle_normal.vt3"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.vc1" "face_dx11_wrinkle_normal.vc1"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.o" "face_dx11_wrinkle_normal.uv"
		;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.ofs" "face_dx11_wrinkle_normal.fs"
		;
connectAttr ":defaultColorMgtGlobals.cme" "face_dx11_wrinkle_color.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "face_dx11_wrinkle_color.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "face_dx11_wrinkle_color.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "face_dx11_wrinkle_color.ws";
connectAttr "face_dx11_wrinkle_color_place2dTexture.c" "face_dx11_wrinkle_color.c"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.tf" "face_dx11_wrinkle_color.tf"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.rf" "face_dx11_wrinkle_color.rf"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.mu" "face_dx11_wrinkle_color.mu"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.mv" "face_dx11_wrinkle_color.mv"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.s" "face_dx11_wrinkle_color.s"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.wu" "face_dx11_wrinkle_color.wu"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.wv" "face_dx11_wrinkle_color.wv"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.re" "face_dx11_wrinkle_color.re"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.of" "face_dx11_wrinkle_color.of"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.r" "face_dx11_wrinkle_color.ro"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.n" "face_dx11_wrinkle_color.n"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.vt1" "face_dx11_wrinkle_color.vt1"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.vt2" "face_dx11_wrinkle_color.vt2"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.vt3" "face_dx11_wrinkle_color.vt3"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.vc1" "face_dx11_wrinkle_color.vc1"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.o" "face_dx11_wrinkle_color.uv"
		;
connectAttr "face_dx11_wrinkle_color_place2dTexture.ofs" "face_dx11_wrinkle_color.fs"
		;
connectAttr ":defaultColorMgtGlobals.cme" "face_dx11_normal_map.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "face_dx11_normal_map.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "face_dx11_normal_map.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "face_dx11_normal_map.ws";
connectAttr ":defaultColorMgtGlobals.cme" "face_dx11_maskMap4.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "face_dx11_maskMap4.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "face_dx11_maskMap4.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "face_dx11_maskMap4.ws";
connectAttr "face_dx11_maskMap4_place2dTexture.c" "face_dx11_maskMap4.c";
connectAttr "face_dx11_maskMap4_place2dTexture.tf" "face_dx11_maskMap4.tf";
connectAttr "face_dx11_maskMap4_place2dTexture.rf" "face_dx11_maskMap4.rf";
connectAttr "face_dx11_maskMap4_place2dTexture.mu" "face_dx11_maskMap4.mu";
connectAttr "face_dx11_maskMap4_place2dTexture.mv" "face_dx11_maskMap4.mv";
connectAttr "face_dx11_maskMap4_place2dTexture.s" "face_dx11_maskMap4.s";
connectAttr "face_dx11_maskMap4_place2dTexture.wu" "face_dx11_maskMap4.wu";
connectAttr "face_dx11_maskMap4_place2dTexture.wv" "face_dx11_maskMap4.wv";
connectAttr "face_dx11_maskMap4_place2dTexture.re" "face_dx11_maskMap4.re";
connectAttr "face_dx11_maskMap4_place2dTexture.of" "face_dx11_maskMap4.of";
connectAttr "face_dx11_maskMap4_place2dTexture.r" "face_dx11_maskMap4.ro";
connectAttr "face_dx11_maskMap4_place2dTexture.n" "face_dx11_maskMap4.n";
connectAttr "face_dx11_maskMap4_place2dTexture.vt1" "face_dx11_maskMap4.vt1";
connectAttr "face_dx11_maskMap4_place2dTexture.vt2" "face_dx11_maskMap4.vt2";
connectAttr "face_dx11_maskMap4_place2dTexture.vt3" "face_dx11_maskMap4.vt3";
connectAttr "face_dx11_maskMap4_place2dTexture.vc1" "face_dx11_maskMap4.vc1";
connectAttr "face_dx11_maskMap4_place2dTexture.o" "face_dx11_maskMap4.uv";
connectAttr "face_dx11_maskMap4_place2dTexture.ofs" "face_dx11_maskMap4.fs";
connectAttr ":defaultColorMgtGlobals.cme" "face_dx11_maskMap3.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "face_dx11_maskMap3.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "face_dx11_maskMap3.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "face_dx11_maskMap3.ws";
connectAttr "face_dx11_maskMap3_place2dTexture.c" "face_dx11_maskMap3.c";
connectAttr "face_dx11_maskMap3_place2dTexture.tf" "face_dx11_maskMap3.tf";
connectAttr "face_dx11_maskMap3_place2dTexture.rf" "face_dx11_maskMap3.rf";
connectAttr "face_dx11_maskMap3_place2dTexture.mu" "face_dx11_maskMap3.mu";
connectAttr "face_dx11_maskMap3_place2dTexture.mv" "face_dx11_maskMap3.mv";
connectAttr "face_dx11_maskMap3_place2dTexture.s" "face_dx11_maskMap3.s";
connectAttr "face_dx11_maskMap3_place2dTexture.wu" "face_dx11_maskMap3.wu";
connectAttr "face_dx11_maskMap3_place2dTexture.wv" "face_dx11_maskMap3.wv";
connectAttr "face_dx11_maskMap3_place2dTexture.re" "face_dx11_maskMap3.re";
connectAttr "face_dx11_maskMap3_place2dTexture.of" "face_dx11_maskMap3.of";
connectAttr "face_dx11_maskMap3_place2dTexture.r" "face_dx11_maskMap3.ro";
connectAttr "face_dx11_maskMap3_place2dTexture.n" "face_dx11_maskMap3.n";
connectAttr "face_dx11_maskMap3_place2dTexture.vt1" "face_dx11_maskMap3.vt1";
connectAttr "face_dx11_maskMap3_place2dTexture.vt2" "face_dx11_maskMap3.vt2";
connectAttr "face_dx11_maskMap3_place2dTexture.vt3" "face_dx11_maskMap3.vt3";
connectAttr "face_dx11_maskMap3_place2dTexture.vc1" "face_dx11_maskMap3.vc1";
connectAttr "face_dx11_maskMap3_place2dTexture.o" "face_dx11_maskMap3.uv";
connectAttr "face_dx11_maskMap3_place2dTexture.ofs" "face_dx11_maskMap3.fs";
connectAttr ":defaultColorMgtGlobals.cme" "face_dx11_maskMap2.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "face_dx11_maskMap2.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "face_dx11_maskMap2.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "face_dx11_maskMap2.ws";
connectAttr "face_dx11_maskMap2_place2dTexture.c" "face_dx11_maskMap2.c";
connectAttr "face_dx11_maskMap2_place2dTexture.tf" "face_dx11_maskMap2.tf";
connectAttr "face_dx11_maskMap2_place2dTexture.rf" "face_dx11_maskMap2.rf";
connectAttr "face_dx11_maskMap2_place2dTexture.mu" "face_dx11_maskMap2.mu";
connectAttr "face_dx11_maskMap2_place2dTexture.mv" "face_dx11_maskMap2.mv";
connectAttr "face_dx11_maskMap2_place2dTexture.s" "face_dx11_maskMap2.s";
connectAttr "face_dx11_maskMap2_place2dTexture.wu" "face_dx11_maskMap2.wu";
connectAttr "face_dx11_maskMap2_place2dTexture.wv" "face_dx11_maskMap2.wv";
connectAttr "face_dx11_maskMap2_place2dTexture.re" "face_dx11_maskMap2.re";
connectAttr "face_dx11_maskMap2_place2dTexture.of" "face_dx11_maskMap2.of";
connectAttr "face_dx11_maskMap2_place2dTexture.r" "face_dx11_maskMap2.ro";
connectAttr "face_dx11_maskMap2_place2dTexture.n" "face_dx11_maskMap2.n";
connectAttr "face_dx11_maskMap2_place2dTexture.vt1" "face_dx11_maskMap2.vt1";
connectAttr "face_dx11_maskMap2_place2dTexture.vt2" "face_dx11_maskMap2.vt2";
connectAttr "face_dx11_maskMap2_place2dTexture.vt3" "face_dx11_maskMap2.vt3";
connectAttr "face_dx11_maskMap2_place2dTexture.vc1" "face_dx11_maskMap2.vc1";
connectAttr "face_dx11_maskMap2_place2dTexture.o" "face_dx11_maskMap2.uv";
connectAttr "face_dx11_maskMap2_place2dTexture.ofs" "face_dx11_maskMap2.fs";
connectAttr ":defaultColorMgtGlobals.cme" "face_dx11_maskMap1.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "face_dx11_maskMap1.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "face_dx11_maskMap1.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "face_dx11_maskMap1.ws";
connectAttr "face_dx11_maskMap1_place2dTexture.c" "face_dx11_maskMap1.c";
connectAttr "face_dx11_maskMap1_place2dTexture.tf" "face_dx11_maskMap1.tf";
connectAttr "face_dx11_maskMap1_place2dTexture.rf" "face_dx11_maskMap1.rf";
connectAttr "face_dx11_maskMap1_place2dTexture.mu" "face_dx11_maskMap1.mu";
connectAttr "face_dx11_maskMap1_place2dTexture.mv" "face_dx11_maskMap1.mv";
connectAttr "face_dx11_maskMap1_place2dTexture.s" "face_dx11_maskMap1.s";
connectAttr "face_dx11_maskMap1_place2dTexture.wu" "face_dx11_maskMap1.wu";
connectAttr "face_dx11_maskMap1_place2dTexture.wv" "face_dx11_maskMap1.wv";
connectAttr "face_dx11_maskMap1_place2dTexture.re" "face_dx11_maskMap1.re";
connectAttr "face_dx11_maskMap1_place2dTexture.of" "face_dx11_maskMap1.of";
connectAttr "face_dx11_maskMap1_place2dTexture.r" "face_dx11_maskMap1.ro";
connectAttr "face_dx11_maskMap1_place2dTexture.n" "face_dx11_maskMap1.n";
connectAttr "face_dx11_maskMap1_place2dTexture.vt1" "face_dx11_maskMap1.vt1";
connectAttr "face_dx11_maskMap1_place2dTexture.vt2" "face_dx11_maskMap1.vt2";
connectAttr "face_dx11_maskMap1_place2dTexture.vt3" "face_dx11_maskMap1.vt3";
connectAttr "face_dx11_maskMap1_place2dTexture.vc1" "face_dx11_maskMap1.vc1";
connectAttr "face_dx11_maskMap1_place2dTexture.o" "face_dx11_maskMap1.uv";
connectAttr "face_dx11_maskMap1_place2dTexture.ofs" "face_dx11_maskMap1.fs";
connectAttr ":defaultColorMgtGlobals.cme" "face_dx11_diffuse_map.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "face_dx11_diffuse_map.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "face_dx11_diffuse_map.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "face_dx11_diffuse_map.ws";
connectAttr "face_dx11_maskMap4.oc" "SkinShader.Mask4_";
connectAttr "face_dx11_maskMap3.oc" "SkinShader.Mask3_";
connectAttr "face_dx11_maskMap2.oc" "SkinShader.Mask2_";
connectAttr "face_dx11_maskMap1.oc" "SkinShader.Mask1_";
connectAttr "face_dx11_wrinkle_color.oc" "SkinShader.CavityTexture1";
connectAttr "face_dx11_wrinkle_normal.oc" "SkinShader.CompExpTexture1";
connectAttr "face_dx11_diffuse_map.oc" "SkinShader.DiffuseTexture";
connectAttr "face_dx11_normal_map.oc" "SkinShader.NormalTexture";
connectAttr "dx11Shader8SG.pa" ":renderPartition.st" -na;
connectAttr "SkinShader.msg" ":defaultShaderList1.s" -na;
connectAttr "face_dx11_wrinkle_normal_place2dTexture.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "face_dx11_wrinkle_color_place2dTexture.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "face_dx11_maskMap1_place2dTexture.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "face_dx11_maskMap2_place2dTexture.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "face_dx11_maskMap3_place2dTexture.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "face_dx11_maskMap4_place2dTexture.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "face_dx11_diffuse_map.msg" ":defaultTextureList1.tx" -na;
connectAttr "face_dx11_normal_map.msg" ":defaultTextureList1.tx" -na;
connectAttr "face_dx11_wrinkle_normal.msg" ":defaultTextureList1.tx" -na;
connectAttr "face_dx11_wrinkle_color.msg" ":defaultTextureList1.tx" -na;
connectAttr "face_dx11_maskMap1.msg" ":defaultTextureList1.tx" -na;
connectAttr "face_dx11_maskMap2.msg" ":defaultTextureList1.tx" -na;
connectAttr "face_dx11_maskMap3.msg" ":defaultTextureList1.tx" -na;
connectAttr "face_dx11_maskMap4.msg" ":defaultTextureList1.tx" -na;
dataStructure -fmt "raw" -as "name=faceConnectOutputStructure:bool=faceConnectOutput:string[200]=faceConnectOutputAttributes:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=idStructure:int32=ID";
dataStructure -fmt "raw" -as "name=faceConnectMarkerStructure:bool=faceConnectMarker:string[200]=faceConnectOutputGroups";
// End of DX11.ma
