import { Building, Calendar, Link, MapPin } from "lucide-react";
import InfoItem from "../Common/InfoItem";

export default function UserProfile({ userData }) {
  const { data } = userData;

  return (
    <>
      <div className="github-card p-6">
        <div className="flex items-start space-x-4">
          <img
            src={data.avatar_url}
            alt={data.username}
            className="w-20 h-20 rounded-full border-2 border-primary-600"
          />
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2">
              <h2 className="text-2xl font-bold">
                {data.name || data.username}
              </h2>
              <span
                className={`skill-badge skill-${data.skill_level} px-3 py-1 rounded-full text-xs font-semibold text-white`}
              >
                {data.skill_level}
              </span>
            </div>
            <p className="text-github-text-secondary mb-4">@{data.username}</p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <InfoItem
                icon={<Calendar className="w-4 h-4" />}
                label="Joined"
                value={new Date(data.joined_date).toLocaleDateString()}
              />
              <InfoItem
                icon={<MapPin className="w-4 h-4" />}
                label="Location"
                value={data.location || "Not specified"}
              />
              <InfoItem
                icon={<Building className="2-4 h-4" />}
                label="Company"
                value={data.company || "Not specified"}
              />
              <InfoItem
                icon={<Link className="w-4 h-4" />}
                label="Blog"
                value={data.blog ? "Yes" : "No"}
              />
            </div>
            {data.bio && (
              <p className="text-github-text-secondary border-t border-github-border pt-4">
                {data.bio}
              </p>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
