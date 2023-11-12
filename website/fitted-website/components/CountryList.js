"use client";
import { useEffect, useState } from 'react';
import { supabase } from '../lib/initSupabase';

export default function CountryList() {
  const [countries, setCountries] = useState([]);

  useEffect(() => {
    fetchCountries();
  }, []);

  const fetchCountries = async () => {
    try {
      const { data: countries, error } = await supabase
        .from('countries')
        .select('*')
        .order('name', true);

      if (error) {
        // Handle the error, e.g., log it or show an error message
        console.error('Error fetching countries:', error.message);
        return;
      }

      // Set countries only if the data is available
      if (countries) {
        setCountries(countries);
      }
    } catch (error) {
      console.error('Error fetching countries:', error.message);
    }
  };

  return (
    <div>
      {countries.length > 0 ? (
        countries.map((country) => (
          <li key={country.id}>{country.name}</li>
        ))
      ) : (
        <p>No countries available</p>
      )}
    </div>
  );
}