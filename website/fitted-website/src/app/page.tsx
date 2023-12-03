import Image from 'next/image'
import Head from 'next/head'
import CountryList from '../../components/CountryList'

export default function Home() {
  return (
    <main>
      <CountryList />
    </main>
  );
}