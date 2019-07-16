#!/bin/bash
# version 7/12/19

# DISCLAIMER OF WARRANTY
#This document may contain the following HPE or other software: XML, CLI statements, scripts, parameter files. These are provided as a courtesy, 
#free of charge, AS-IS by Hewlett-Packard Enterprise Company (HPE). HPE shall have no obligation to maintain or support this software. HPE MAKES
#NO EXPRESS OR IMPLIED WARRANTY OF ANY KIND REGARDING THIS SOFTWARE INCLUDING ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, 
#TITLE OR NON-INFRINGEMENT. HPE SHALL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES, WHETHER BASED ON CONTRACT,
#TORT OR ANY OTHER LEGAL THEORY, CONNECTION WITH OR ARISING OUT OF THE FURNISHING, PERFORMANCE OR USE OF THIS SOFTWARE.

#Copyright 2011 Hewlett-Packard Enterprise Development Company, L.P. The information contained herein is subject to change without notice. The only
#warranties for HPE products and services are set forth in the express warranty statements accompanying such products and services. Nothing
#herein should be construed as constituting an additional warranty. HPE shall not be liable for technical or editorial errors or omissions 
#contained herein.



function set_values {
    AutoID=$(( $RANDOM % ${car_count_arg} + 1 ))

     ############################
     #EventCategoryID
     ############################
     index=$(( $RANDOM % ${EventCategoryID_max} ))
     EventCategoryID=${EventCategoryIDs[$index]}

     ############################
     #City 
     ############################
     index=$(( $RANDOM % ${city_max} ))
     city=${cities[$index]}

     ############################
     #OutsideTemperature 
     ############################
     index=$(( $RANDOM % 90 ))
     if [ "$city" == "Seattle" ]
      then
         probability="1.2"
      else
         probability="0.3"
     fi
     OutsideTemperature=$(awk "BEGIN{print int(($index ** $probability))}")

     ############################
     #EngineTemperature 
     ############################
     index=$(( $RANDOM % 180 + 50 ))
     if [ "$city" == "Seattle" ]
      then
         probability="1.2"
      else
         probability="0.3"
     fi
     EngineTemperature=$(awk "BEGIN{print int(($index ** $probability))}")

     ############################
     #Speed 
     ############################
     index=$(( $RANDOM % 100 ))
     if [ "$city" == "Bellevue" ]
      then
         probability=".5"
      else
         probability="0.9"
     fi
     Speed=$(awk "BEGIN{print int(($index ** $probability))}")

     ############################
     #Fuel 
     ############################
     Fuel=$(( $RANDOM % 40 ))

     ############################
     #EngineOil 
     ############################
     index=$(( $RANDOM % 50 ))
     if [ "$city" == "Seattle" ]
      then
         probability="1.2"
      else
         probability="0.3"
     fi
     EngineOil=$(awk "BEGIN{print int(($index ** $probability))}")

     ############################
     #TirePressure 
     ############################
     index=$(( $RANDOM % 35 ))
     if [ "$city" == "Seattle" ]
      then
         probability="0.5"
      else
         probability="1.7"
     fi
     TirePressure=$(awk "BEGIN{print int(($index ** $probability))}")

     ############################
     #ParkingBrakeStatus 
     ############################
     index=$(( $RANDOM % 2 ))
     if [ $index == 0 ]
     then 
       ParkingBrakeStatus="TRUE"
     else
       ParkingBrakeStatus="FALSE"
     fi

     ############################
     #HeadlampStatus 
     ############################
     index=$(( $RANDOM % 2 ))
     if [ $index == 0 ]
     then 
       HeadlampStatus="TRUE"
     else
       HeadlampStatus="FALSE"
     fi

     ############################
     #TransmissionGearPosition 
     ############################
     TransmissionGearPosition=$(( $RANDOM % 8 + 1 ))

     ############################
     #IgnitionStatus 
     ############################
     index=$(( $RANDOM % 2 ))
     if [ $index == 0 ]
     then 
       IgnitionStatus="TRUE"
     else
       IgnitionStatus="FALSE"
     fi

     ############################
     #WindshieldWiperStatus 
     ############################
     index=$(( $RANDOM % 2 ))
     if [ $index == 0 ]
     then 
       WindshieldWiperStatus="TRUE"
     else
       WindshieldWiperStatus="FALSE"
     fi

     ############################
     #PostalCode 
     ############################
     index=$(( $RANDOM % ${zipcode_max} ))
     PostalCode=${zipcodes[$index]}

     Odometer=$(( $RANDOM % 5000 ))

     ############################
     #Timestamp 
     ############################
     Date_Timestamp=`date '+%Y-%m-%d %H:%M:%S.%N'`
} 

function gen_iot_stream {
  rowcount=1

   readarray -t zipcodes  < $currentpath_arg/data/zipcodes.csv
   zipcode_max=${#zipcodes[@]}
   let zipcode_max--
  
   cities=("Seattle" "Redmond" "Bellevue" "Sammamish" "Bellevue" "Bellevue" "Seattle" "Seattle" "Seattle" "Redmond" "Bellevue" "Redmond")
   city_max=${#cities[@]}
   let city_max--

   if [ -f "${output_loc_arg}/data/iotcar_stream/iotcar_stream${file_id_arg}.csv" ]
    then
      rm -f $output_loc_arg}/data/iotcar_stream/iotcar_stream${file_id_arg}.csv
    fi

# seed random
   index=$(( $RANDOM % ${file_row_count_arg} ))
   c_date=`date '+%Y-%m-%d %H:%M:%S.%N'` 

#EventCategoryID
   EventCategoryIDs=(3 3 3 3 3 3 2 3 3 3)
   EventCategoryID_max=${#EventCategoryIDs[@]}
   let eventCategoryId_max--
 
   let EventID=( ${file_id_arg} * ${file_row_count_arg} ) 

   set_values

################################
##  start if generation loop
################################
   for (( x=1; x<=$file_row_count_arg; x++ ))
    do  

     ############################
     #EventID   Guid
     ############################
     let EventID++

     ############################
     #EventCategoryID
     ############################
 
     index=$(( $RANDOM % ${EventCategoryID_max} ))
     EventCategoryID=${EventCategoryIDs[$index]}

     ############################
     # EventMessage
     ############################

     if [ $EventCategoryID -eq 3 ]
     then
       EventMessage="Informational"
       Abs="FALSE"
       index=$(( $RANDOM % 2 ))
       if [ $index == 0 ]
        then 
         BrakePedalStatus="TRUE"
       else
         BrakePedalStatus="FALSE"
       fi
     else
       EventMessage="Safety"
       Abs="TRUE"
       BrakePedalStatus="TRUE"
     fi

     ############################
     #Odometer 
     ############################
     let Odometer=(${Odometer} + 1)

     ############################
     #AcceleratorPedalPosition 
     ############################
     AcceleratorPedalPosition=$(( $RANDOM % 100 ))

  
#   echo  $EventID $AutoID $EventCategoryID $EventMessage $city $OutsideTemperature $EngineTemperature $Speed $Fuel $EngineOil $TirePressure  $Odometer $AcceleratorPedalPosition $ParkingBrakeStatus $HeadlampStatus $BrakePedalStatus $TransmissionGearPosition $IgnitionStatus $WindshieldWiperStatus $Abs $PostalCode $Date_Timestamp

# write 1000 rows 

#     printf -v newrow "%i|%i|%i|%.20s|%.50s|%i|%i|%i|%i|%i|%i|%i|%i|%.5s|%.5s|%.5s|%i|%.5s|%.5s|%.5s|%.5s|%.30s \n" "$EventID" "$AutoID" "$EventCategoryID" "$EventMessage" "$city" "$OutsideTemperature" "$EngineTemperature" "$Speed" "$Fuel" "$EngineOil" "$TirePressure" "$Odometer" "$AcceleratorPedalPosition" "$ParkingBrakeStatus" "$HeadlampStatus" "$BrakePedalStatus" "$TransmissionGearPosition" "$IgnitionStatus" "$WindshieldWiperStatus" "$Abs" "$PostalCode" "$Date_Timestamp" # >> ${output_loc_arg}/data/iotcar_stream/iotcar_stream${file_id_arg}.csv
     printf "%i|%i|%i|%.20s|%.50s|%i|%i|%i|%i|%i|%i|%i|%i|%.5s|%.5s|%.5s|%i|%.5s|%.5s|%.5s|%.5s|%.30s \n" "$EventID" "$AutoID" "$EventCategoryID" "$EventMessage" "$city" "$OutsideTemperature" "$EngineTemperature" "$Speed" "$Fuel" "$EngineOil" "$TirePressure" "$Odometer" "$AcceleratorPedalPosition" "$ParkingBrakeStatus" "$HeadlampStatus" "$BrakePedalStatus" "$TransmissionGearPosition" "$IgnitionStatus" "$WindshieldWiperStatus" "$Abs" "$PostalCode" "$Date_Timestamp"  >> ${output_loc}/data/iotcar_stream/iotcar_stream${file_id_arg}.csv
#     allrows="$allrows $newrow"

     if [ $rowcount -gt 1000 ]
     then
#       echo "$allrows" >> ${currentpath_arg}/data/iotcar_stream/iotcar_stream${file_id_arg}.csv
#       allrows=""
       rowcount=1
       set_values
     else
       let rowcount++
     fi
  done  
}

function gen_names {
   readarray -t firstnames  < $currentpath/data/firstname.csv
   firstname_max=${#firstnames[@]}
   let firstname_max--

   readarray -t lastnames  < $currentpath/data/lastname.csv
   lastname_max=${#lastnames[@]}
   let lastname_max--

   PhoneNumber="415-123-1234"
   FaxNumber="415-123-1234"

   if [ -f "${output_loc}/data/owners/owners.csv" ]
    then
      rm -f ${output_loc}/data/owners/owners.csv
   fi

   for (( count=1; count<=$name_count; count++ ))
    do
      PersonID=${count} 
      first_index=$(( $RANDOM % ${firstname_max} ))
      last_index=$(( $RANDOM % ${lastname_max} ))
      FullName="${firstnames[$first_index]} ${lastnames[$last_index]}" 
      PreferredName=${firstnames[$first_index]}
      year=$(( $RANDOM % 62 + 1940 ))
      month=$(( $RANDOM % 12 + 1 ))
      day=$(( $RANDOM % 28 + 1 ))
      DateOfBirth="${year}-${month}-${day}"
      EmailAddress="${firstnames[$first_index]}@iot.com"
      printf "%i|%.50s|%.50s|%.10s|%.20s|%.20s|%.75s \n" ${PersonID} "${FullName}" "${PreferredName}" "${DateOfBirth}" "${PhoneNumber}" "${FaxNumber}" "${EmailAddress}" >> ${output_loc}/data/owners/owners.csv

   done
}

function gen_vehicles {

   Makes=("Chevrolet" "Ford" "BMW" "Mercedes" "Kia" "Toyota" "Jaguar" "GMC" "Subaru" "Cadillac" "Porche")
   Make_max=${#Makes[@]}
   let Model_max--

   Models=("Sedan" "Commercial" "Convertible" "Convertible 2DR" "Coupe" "Crossover" "Hatchback" "Hybrid" "Minivan" "Sedan" "SUV" "Truck" "Wagon")
   Model_max=${#Models[@]}
   let Model_max--

   DriveTrains=("RWD" "FWD" "AWD")
   DriveTrain_max=${#DriveTrains[@]}
   let DriveTrain_max--

   EngineTypes=( "8 Cylinder" "8 Cylinder 12" "Cylinder 3"  "4 Cylinder" "4 Cylinder" "4 Cylinder" "6 Cylinder" "6 Cylinder" "Hybrid Electric")
   EngineType_max=${#EngineTypes[@]}
   let EngineType_max--

   ExteriorColors=("Black" "Blazing Gray" "Blue" "Blue" "Chili Red" "Deep Blue" "Electric Blue" "Gray" "Gray" "Gray" "Midnight Black" "Midnight Black" "Pepper White" "Racing Red" "White" "White" "Red" "Silver" "Volcanic Orange" "Yellow" "White Silver")
   ExteriorColor_max=${#ExteriorColors[@]}
   let ExteriorColor_max--

   InteriorColors=("Beige" "Beige" "Black" "Black" "Brown" "Dark Gray" "Gray" "Ivory" "Nutmeg" "Red" "Smoke White" "White")
   InteriorColor_max=${#InteriorColors[@]}
   let InteriorColor_max--

   Transmissions=("Semi-automatic" "Automatic" "Automatic" "Automatic" "Manual")
   Transmission_max=${#Transmissions[@]}
   let Transmission_max--

   if [ -f "${output_loc}/data/autos/autos.csv" ]
    then
      rm -f ${output_loc}/data/autos/autos.csv
   fi

   ownerid_count=1

   for (( count=1; count<=$car_count; count++ ))
   do
     AutoID=$count
     OwnerID=${ownerid_count}
     let ownerid_count++
     if [ ${ownerid_count} -gt $name_count ] 
      then
       ownerid_count=1
      fi
    
     vin=`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w ${1:-20} | head -n 1`
    
     index=$(( $RANDOM % ${Make_max} ))
     Make=${Makes[$index]}

     index=$(( $RANDOM % ${Model_max} ))
     Model=${Models[$index]}

     year=$(( $RANDOM % 46 + 1972 ))

     index=$(( $RANDOM % ${DriveTrain_max} ))
     DriveTrain=${DriveTrains[$index]}

     index=$(( $RANDOM % ${EngineType_max} ))
     EngineType=${EngineTypes[$index]}

     index=$(( $RANDOM % ${ExteriorColor_max} ))
     ExteriorColor=${ExteriorColors[$index]}

     index=$(( $RANDOM % ${InteriorColor_max} ))
     InteriorColor=${InteriorColors[$index]}

     index=$(( $RANDOM % ${Transmission_max} ))
     Transmission=${Transmissions[$index]}
     printf "%i|%i|%.20s|%.30s|%.30s|%.10s|%.10s|%.30s|%.30s|%.30s|%.30s \n" "${AutoID}" "${OwnerID}" "${vin}" "${Make}" "${Model}" "${year}" "${DriveTrain}" "${EngineType}" "${ExteriorColor}" "${InteriorColor}" "${Transmission}" >> ${output_loc}/data/autos/autos.csv

  done
} 

function show_help {

  echo ""
  echo "IoT Connected Car Data Generator"
  echo ""
  echo "Arguments:"
  echo "   -streams    Number of concurrent streams("${parallel_streams}")" 
  echo "   -file_size  Individual file size in Mb ("${file_size}")"
  echo "   -total_size Total file file size in Mb ("${target_size}")"
  echo "   -out_loc    Location to create files"
  echo "   -h          Show this help message and exit"
  echo ""
  exit 

}


#define parallel stream count
parallel_streams=10
#target total data size mb
target_size=1000
#target individual file size Mb
file_size=10 
thishost=`hostname`
currentpath=`pwd`
output_loc=`pwd`
genstreamflag=FALSE


name_count=10000
car_count=20000

while [ "$1" != "" ]; do
    case $1 in
       -h | -help  )            show_help;;
        -genstream  )           shift
                                genstreamflag=${1}
                                shift;;
        -output_loc_arg  )      shift
                                output_loc=${1}
                                shift;;
        -file_row_count_arg  )  shift
                                file_row_count_arg=${1}
                                shift;;
        -file_id_arg  )         shift
                                file_id_arg=${1}
                                shift;;
        -currentpath_arg  )     shift
                                currentpath_arg=${1}
                                shift;;
        -car_count_arg  )       shift
                                car_count_arg=${1}
                                shift;;
        -streams  )             shift
                                parallel_streams=${1}
                                shift;;
        -file_size )             shift
                                file_size=${1}
                                shift;;
        -out_loc )              shift
                                output_loc=${1}
                                shift;;
        -total_size )           shift
                                target_size=${1}
                                shift;;
         ?* )                   show_help;;
    esac
done

#convert to bytes
   let "target_size=$target_size * 1000000"
   let "file_size=$file_size * 1000000"

   if [ "$target_size" -lt "$file_size" ];then
     target_size=${file_size}
   fi

   let "file_row_count=$file_size / 120"

   let "total_count=$target_size / $file_size"

   driver_count=$total_count

   if [ "$total_count" -lt "$parallel_streams" ]
     then
      parallel_streams=$total_count
#   else
#     let "total_count=$total_count / $parallel_streams"
   fi

if [ "$genstreamflag" = "FALSE" ];then

  echo ""
  echo "Parallel streams " $parallel_streams
  echo "File size " $file_size
  echo "Output location " $output_loc
  echo ""

#create directories

  if [ ! -d "${output_loc}/data/" ]; then

     if mkdir -p ${output_loc}/data; then
      echo "Created directory ${output_loc}/data"
     else
      echo "Cannot continue ${output_loc}/data not found"
      exit
     fi

  fi

  if [ ! -d "${output_loc}/data/iotcar_stream/" ]; then

     if mkdir -p ${output_loc}/data/iotcar_stream;then
      echo "Created directory ${output_loc}/iotcar_stream"
     else
      echo "Cannot continue ${output_loc}/iot_stream not found"
      exit
     fi     

  fi

  if [ ! -d "${output_loc}/data/owners/" ]; then

     if mkdir -p ${output_loc}/data/owners; then
      echo "Created directory ${output_loc}/owners"
     else
      echo "Cannot continue ${output_loc}/owners not found"
      exit
     fi

  fi

  if [ ! -d "${output_loc}/data/autos/" ]; then

     if mkdir -p ${output_loc}/data/autos; then
      echo "Created directory ${output_loc}/autos"
      echo " "
     else
      echo "Cannot continue ${output_loc}/autos not found"
      exit 
    fi

  fi

# Gen names


  ${currentpath}/geniotdata.sh -genstream GENNAMES -car_count_arg ${car_count} -output_loc_arg ${output_loc} -file_row_count_arg ${file_row_count} -currentpath_arg ${currentpath} &

# Gen cars
  ${currentpath}/geniotdata.sh -genstream GENCAR   -car_count_arg ${car_count} -output_loc_arg ${output_loc} -file_row_count_arg ${file_row_count}  -currentpath_arg ${currentpath} &

# wait for these to complete
  wait

# Start Stream Generation
 ${currentpath}/geniotdata.sh -genstream GENIOT -car_count_arg ${car_count} -output_loc_arg ${output_loc} -file_row_count_arg ${file_row_count} -currentpath_arg ${currentpath} 

fi # end gen streams = FALSE

if [ "$genstreamflag" = "GENNAMES" ];then
 # Gen Names
    echo "Generating ${name_count} Names"
    gen_names
fi
   
# Gen vehicles
if [ "$genstreamflag" = "GENCAR" ];then
   echo "Generating ${car_count} Vehicles"
   gen_vehicles
fi


if [ "$genstreamflag" = "GENIOT" ];then

# start iot generation
   echo ""
   echo "Target File Size: $target_size "
   echo "Individual File Size: $file_size " 
   echo "Number of drivers required: $total_count "
   echo ""

  file_count=0
  file_id=1

# loop to gen
  while (( $file_id<=$total_count ))
    do
    let "file_count=$file_count + $parallel_streams"  
    echo "Generating IoT Data  $file_count  of $total_count"
    driver_count=1
     while (( $driver_count<=$parallel_streams &&  $file_id<=$total_count ))
#     for (( count=1; count<=$parallel_streams; count++ ))
      do
        ${currentpath}/geniotdata.sh -genstream GENDATA -car_count_arg ${car_count} -output_loc_arg ${output_loc} -file_row_count_arg ${file_row_count} -file_id_arg ${file_id} -currentpath_arg ${currentpath} &
        let file_id++
        let driver_count++
      done 
      wait
  done
fi

# Generate Data
if [ "$genstreamflag" = "GENDATA" ];then
  gen_iot_stream
fi
