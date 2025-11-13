import { useParams } from "react-router-dom";

const ProductPage = () => {
  const { id } = useParams();
  return (
    <div className="p-8">
      <h2 className="text-2xl font-semibold">Product Details — ID: {id}</h2>
      <p>This page will show full product details.</p>
    </div>
  );
};

export default ProductPage;
