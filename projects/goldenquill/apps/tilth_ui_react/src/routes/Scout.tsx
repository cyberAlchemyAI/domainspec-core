import { useEffect, useState } from 'react';
import { SubstrateClient } from '../api/SubstrateClient';

export default function Scout({ substrate }: { substrate: SubstrateClient }) {
  const [projection, setProjection] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    substrate.getProjection().then(data => {
      setProjection(data);
      setLoading(false);
    });
  }, [substrate]);

  if (loading) return <div>Loading Scout Data...</div>;

  return (
    <div className="card">
      <h2>Scout Opportunities</h2>
      <pre>{JSON.stringify(projection?.scout || {}, null, 2)}</pre>
    </div>
  );
}
