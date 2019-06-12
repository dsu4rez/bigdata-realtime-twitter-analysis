package com.davidiscoding.flumetwittersource;

public class TwitterQueryParameterParser {

	private  String[] getValuesFromCSV(String csvString){
		String [] values;

		if (csvString.trim().length() == 0) {
			values = new String[0];
		} else {
			values = csvString.split(",");
			for (int i = 0; i < values.length; i++) {
				values[i] = values[i].trim();
			}
		}
		
		return values;
	}
	
	public String[] getKeywords(String keywordsString) {
		return getValuesFromCSV(keywordsString);
	}
	
	public long[] getFollows(String followString) {
		
		String [] followStringValues = getValuesFromCSV(followString);
		int nValues = followStringValues.length;
		long [] follow = new long[nValues];
		
		if(nValues <= 0)
			return follow;
		
		for (int i = 0; i < nValues; i++){
			follow[i] = Long.parseLong(followStringValues[i]);	
		}
		
		return follow;
	}
	
	public double[][] getLocations(String locationString) {
		
		String [] locationStringValues = getValuesFromCSV(locationString);
		int nValues = locationStringValues.length;
		
		if(nValues % 2 != 0) 
			return new double[0][0];
		
		double [][] locations = new double[nValues/2][nValues/2];
		
		int pairCount = 0;
		for(int i = 0; i < nValues; i++){
			if(i % 2 == 0){
				locations[pairCount][0] = Double.parseDouble(locationStringValues[i]);
			}else{
				locations[pairCount][1] = Double.parseDouble(locationStringValues[i]);
				pairCount++;
			}
		}
		
		return locations;
		
	} 
}
